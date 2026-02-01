#!/usr/bin/env python3

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Tuple
import datetime as _dt


def _stamp() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")


def _default_out_dir() -> str:
    projects_tmp = os.path.expanduser("~/Projects/tmp")
    if os.path.isdir(projects_tmp):
        return os.path.join(projects_tmp, f"beauty-generation-{_stamp()}")
    return os.path.join(os.getcwd(), "tmp", f"beauty-generation-{_stamp()}")


class BeautyAPIClient:
    def __init__(self, api_base: str = "https://gen1.diversityfaces.org", 
                 api_key: str = "ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI"):
        self.api_base = api_base.rstrip("/")
        self.api_key = api_key
        self.timeout = 30

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request with API key authentication."""
        url = f"{self.api_base}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "User-Agent": "beauty-generation-skill/1.0.0"
        }
        
        body = None
        if data:
            body = json.dumps(data).encode("utf-8")
        
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                response_data = resp.read()
                return json.loads(response_data.decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_data = e.read().decode("utf-8")
            try:
                error_json = json.loads(error_data)
                if e.code == 401:
                    raise SystemExit(f"Authentication failed: {error_json.get('message', 'Invalid API key')}")
                elif e.code == 429:
                    raise SystemExit(f"Rate limit exceeded: {error_json.get('message', 'Too many requests')}")
                else:
                    raise SystemExit(f"API error {e.code}: {error_json.get('error', error_data)}")
            except json.JSONDecodeError:
                raise SystemExit(f"HTTP {e.code}: {error_data}")
        except Exception as e:
            raise SystemExit(f"Request failed: {e}")

    def generate_standard(self, **params) -> Dict:
        """Generate with standard parameters."""
        return self._make_request("POST", "/api/generate", params)

    def generate_random(self, **params) -> Dict:
        """Generate with random parameters."""
        return self._make_request("POST", "/api/generate/random", params)

    def generate_custom(self, full_prompt: str, **params) -> Dict:
        """Generate with custom prompt."""
        data = {"full_prompt": full_prompt, **params}
        return self._make_request("POST", "/api/generate/custom", data)

    def check_status(self, prompt_id: str) -> Dict:
        """Check generation status."""
        return self._make_request("GET", f"/api/status/{prompt_id}")

    def get_presets(self) -> Dict:
        """Get available parameter presets."""
        return self._make_request("GET", "/api/presets")

    def download_image(self, filename: str, save_path: str, **params) -> str:
        """Download generated image with improved error handling."""
        url_params = "&".join([f"{k}={v}" for k, v in params.items() if v])
        url = f"{self.api_base}/api/image/{filename}"
        if url_params:
            url += f"?{url_params}"
        
        headers = {
            "X-API-Key": self.api_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # Download image data
                image_data = resp.read()
                
                # Write to file
                with open(save_path, "wb") as f:
                    f.write(image_data)
                
                print(f"Downloaded: {save_path} ({len(image_data):,} bytes)")
                return save_path
        except urllib.error.HTTPError as e:
            error_data = e.read()
            try:
                error_text = error_data.decode("utf-8")
                if "cloudflare" in error_text.lower():
                    raise SystemExit(f"Image download blocked by protection. Try again later.")
                raise SystemExit(f"HTTP {e.code}: Failed to download image - {error_text[:100]}")
            except UnicodeDecodeError:
                raise SystemExit(f"HTTP {e.code}: Failed to download image")
        except Exception as e:
            raise SystemExit(f"Failed to download image: {e}")

    def wait_for_completion(self, prompt_id: str, max_wait: int = 300) -> Dict:
        """Wait for generation to complete with robust error handling."""
        start_time = time.time()
        retry_count = 0
        max_retries = 3
        
        print(f"Waiting for completion (max {max_wait}s)...")
        
        while time.time() - start_time < max_wait:
            try:
                # Use a more robust status check
                status = self._check_status_robust(prompt_id)
                
                if status["status"] == "completed":
                    print("✅ Generation completed!")
                    return status
                elif status["status"] == "failed":
                    raise SystemExit(f"Generation failed: {status.get('message', 'Unknown error')}")
                elif status["status"] == "error":
                    if retry_count < max_retries:
                        retry_count += 1
                        print(f"Status check error, retrying ({retry_count}/{max_retries})...")
                        time.sleep(5)
                        continue
                    else:
                        raise SystemExit(f"Status check failed after {max_retries} retries")
                
                print(f"Status: {status['status']} - {status.get('message', 'Processing...')}")
                retry_count = 0  # Reset retry count on successful request
                
            except SystemExit:
                raise
            except Exception as e:
                if retry_count < max_retries:
                    retry_count += 1
                    print(f"Status check error, retrying ({retry_count}/{max_retries}): {e}")
                    time.sleep(5)
                    continue
                else:
                    raise SystemExit(f"Status check failed after {max_retries} retries: {e}")
            
            time.sleep(3)
        
        raise SystemExit(f"Generation timeout after {max_wait} seconds")
    
    def _check_status_robust(self, prompt_id: str) -> Dict:
        """Robust status check with multiple encoding attempts."""
        url = f"{self.api_base}/api/status/{prompt_id}"
        headers = {
            "X-API-Key": self.api_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Accept-Charset": "utf-8"
        }
        
        req = urllib.request.Request(url, headers=headers, method="GET")
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                response_data = resp.read()
                
                # Try multiple encodings
                for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'latin1']:
                    try:
                        text = response_data.decode(encoding)
                        return json.loads(text)
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        continue
                
                # If all encodings fail, return error status
                return {"status": "error", "message": "Failed to decode response"}
                
        except urllib.error.HTTPError as e:
            error_data = e.read()
            
            # Try to decode error response
            error_text = ""
            for encoding in ['utf-8', 'gbk', 'latin1']:
                try:
                    error_text = error_data.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if "cloudflare" in error_text.lower() or "<html" in error_text.lower():
                return {"status": "error", "message": "Server protection detected"}
            
            try:
                error_json = json.loads(error_text)
                return {"status": "error", "message": error_json.get("error", "API error")}
            except json.JSONDecodeError:
                return {"status": "error", "message": f"HTTP {e.code}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}


def load_style_presets() -> Dict[str, Dict]:
    """Load predefined style combinations."""
    return {
        "professional-chinese": {
            "style": "知性",
            "age": "25",
            "nationality": "中国",
            "clothing": "西装",
            "clothing_color": "黑色",
            "scene": "办公室",
            "mood": "自信"
        },
        "traditional-japanese": {
            "style": "古典",
            "age": "23",
            "nationality": "日本",
            "clothing": "和服",
            "clothing_color": "粉色",
            "scene": "花园",
            "mood": "温柔"
        },
        "modern-korean": {
            "style": "现代",
            "age": "20",
            "nationality": "韩国",
            "clothing": "连衣裙",
            "clothing_color": "白色",
            "scene": "城市",
            "mood": "活泼"
        },
        "elegant-chinese-qipao": {
            "style": "优雅",
            "age": "24",
            "nationality": "中国",
            "clothing": "旗袍",
            "clothing_color": "红色",
            "scene": "室内",
            "mood": "高贵"
        },
        "casual-lifestyle": {
            "style": "清纯",
            "age": "22",
            "nationality": "中国",
            "clothing": "休闲装",
            "clothing_color": "蓝色",
            "scene": "咖啡厅",
            "mood": "甜美"
        },
        "fashion-editorial": {
            "style": "冷艳",
            "age": "26",
            "nationality": "俄罗斯",
            "clothing": "晚礼服",
            "clothing_color": "黑色",
            "scene": "城市",
            "mood": "神秘"
        },
        "brazilian-beach": {
            "style": "性感",
            "age": "24",
            "nationality": "巴西",
            "clothing": "连衣裙",
            "clothing_color": "黄色",
            "scene": "海边",
            "mood": "热情"
        },
        "french-elegance": {
            "style": "优雅",
            "age": "27",
            "nationality": "法国",
            "clothing": "外套",
            "clothing_color": "米色",
            "scene": "咖啡厅",
            "mood": "知性"
        },
        "indian-traditional": {
            "style": "古典",
            "age": "22",
            "nationality": "印度",
            "clothing": "民族服装",
            "clothing_color": "红色",
            "scene": "室内",
            "mood": "温柔"
        },
        "american-casual": {
            "style": "活泼",
            "age": "21",
            "nationality": "美国",
            "clothing": "牛仔裤",
            "clothing_color": "蓝色",
            "scene": "公园",
            "mood": "开朗"
        }
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="beauty-generation",
        description="Generate beautiful AI portraits using the Beauty Generation API"
    )
    
    # Generation modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--standard", action="store_true", help="Standard generation with parameters")
    mode_group.add_argument("--random", action="store_true", help="Random generation")
    mode_group.add_argument("--custom", help="Custom prompt generation")
    mode_group.add_argument("--preset", choices=load_style_presets().keys(), help="Use predefined style preset")
    
    # Standard parameters
    parser.add_argument("--style", help="Beauty style (清纯, 性感, 古典, 现代, etc.)")
    parser.add_argument("--age", help="Age (18-28)")
    parser.add_argument("--nationality", help="Nationality/ethnicity")
    parser.add_argument("--clothing", help="Clothing type")
    parser.add_argument("--clothing-color", help="Clothing color")
    parser.add_argument("--scene", help="Background scene")
    parser.add_argument("--mood", help="Emotional expression")
    parser.add_argument("--hair-style", help="Hairstyle")
    parser.add_argument("--hair-color", help="Hair color")
    parser.add_argument("--skin-tone", help="Skin tone")
    parser.add_argument("--accessories", help="Accessories")
    
    # Image parameters
    parser.add_argument("--width", type=int, default=1024, help="Image width (default: 1024)")
    parser.add_argument("--height", type=int, default=1024, help="Image height (default: 1024)")
    parser.add_argument("--seed", type=int, default=-1, help="Random seed (default: -1)")
    
    # Note: Steps are fixed at 4 for security and performance
    
    # Output options
    parser.add_argument("--out-dir", help="Output directory")
    parser.add_argument("--format", default="webp", choices=["png", "webp", "jpeg"], help="Image format")
    parser.add_argument("--count", type=int, default=1, help="Number of images to generate")
    
    # API options
    parser.add_argument("--api-base", default="https://gen1.diversityfaces.org", help="API base URL")
    parser.add_argument("--api-key", help="API key (or use environment variable)")
    parser.add_argument("--timeout", type=int, default=300, help="Generation timeout (seconds)")
    
    # Utility options
    parser.add_argument("--list-presets", action="store_true", help="List available presets")
    parser.add_argument("--show-params", action="store_true", help="Show available parameters")
    parser.add_argument("--dry-run", action="store_true", help="Show parameters without generating")
    
    args = parser.parse_args(argv)
    
    # Handle utility options
    if args.list_presets:
        presets = load_style_presets()
        print("Available style presets:")
        for name, params in presets.items():
            print(f"  {name}:")
            for key, value in params.items():
                print(f"    {key}: {value}")
            print()
        return 0
    
    if args.show_params:
        client = BeautyAPIClient(args.api_base, args.api_key or os.environ.get("BEAUTY_API_KEY"))
        try:
            presets = client.get_presets()
            print("Available parameters:")
            for category, values in presets.items():
                if isinstance(values, list):
                    print(f"  {category}: {', '.join(values[:10])}{'...' if len(values) > 10 else ''}")
        except Exception as e:
            print(f"Failed to fetch parameters: {e}")
            return 1
        return 0
    
    # Initialize client
    api_key = args.api_key or os.environ.get("BEAUTY_API_KEY")
    if not api_key:
        print("Error: API key required. Set BEAUTY_API_KEY environment variable or use --api-key", file=sys.stderr)
        return 1
    
    client = BeautyAPIClient(args.api_base, api_key)
    out_dir = args.out_dir or _default_out_dir()
    os.makedirs(out_dir, exist_ok=True)
    
    # Build generation parameters
    params = {
        "width": args.width,
        "height": args.height,
        "seed": args.seed
    }
    
    # Steps are fixed at 4 for security
    
    # Add style parameters
    style_params = ["style", "age", "nationality", "clothing", "clothing_color", 
                   "scene", "mood", "hair_style", "hair_color", "skin_tone", "accessories"]
    
    for param in style_params:
        value = getattr(args, param.replace("-", "_"))
        if value:
            params[param] = value
    
    # Handle different generation modes
    generations = []
    
    for i in range(args.count):
        if args.preset:
            preset_params = load_style_presets()[args.preset].copy()
            preset_params.update(params)
            if args.dry_run:
                print(f"Preset '{args.preset}' parameters:")
                for key, value in preset_params.items():
                    print(f"  {key}: {value}")
                print("Fixed steps: 4 (for security)")
                continue
            result = client.generate_standard(**preset_params)
            generations.append((result, f"preset-{args.preset}-{i+1}", preset_params))
            
        elif args.standard:
            if args.dry_run:
                print("Standard generation parameters:")
                for key, value in params.items():
                    print(f"  {key}: {value}")
                print("Fixed steps: 4 (for security)")
                continue
            result = client.generate_standard(**params)
            generations.append((result, f"standard-{i+1}", params))
            
        elif args.random:
            if args.dry_run:
                print("Random generation with overrides:")
                for key, value in params.items():
                    if key not in ["width", "height", "seed"]:
                        print(f"  {key}: {value}")
                print("Fixed steps: 4 (for security)")
                continue
            result = client.generate_random(**params)
            generations.append((result, f"random-{i+1}", params))
            
        elif args.custom:
            custom_params = {"full_prompt": args.custom, **params}
            if args.dry_run:
                print(f"Custom generation: {args.custom}")
                print("Fixed steps: 4 (for security)")
                continue
            result = client.generate_custom(args.custom, **params)
            generations.append((result, f"custom-{i+1}", custom_params))
    
    if args.dry_run:
        return 0
    
    # Process generations
    results = []
    for result, name, gen_params in generations:
        if not result.get("success"):
            print(f"Generation failed: {result.get('error', 'Unknown error')}")
            continue
        
        prompt_id = result["prompt_id"]
        print(f"Generated {name} (ID: {prompt_id[:8]}...)")
        print(f"Prompt: {result.get('prompt', 'N/A')}")
        
        # Wait for completion
        try:
            final_status = client.wait_for_completion(prompt_id, args.timeout)
            
            # Download images
            for j, img in enumerate(final_status["images"]):
                filename = img["filename"]
                ext = args.format
                save_name = f"{name}-{j+1}.{ext}"
                save_path = os.path.join(out_dir, save_name)
                
                client.download_image(
                    filename, save_path,
                    format=args.format,
                    subfolder=img.get("subfolder", ""),
                    type=img.get("type", "output")
                )
                
                results.append({
                    "name": name,
                    "file": save_name,
                    "prompt": result.get("prompt", ""),
                    "params": gen_params,
                    "original_filename": filename
                })
                
                print(f"Saved: {save_name}")
        
        except Exception as e:
            print(f"Failed to complete {name}: {e}")
    
    # Save metadata
    if results:
        metadata_path = os.path.join(out_dir, "generation_metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nGenerated {len(results)} images in: {out_dir}")
        print(f"Metadata saved to: generation_metadata.json")
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))