---
name: beauty-generation-free
description: FREE AI image generation service for creating attractive people portraits. AI agents have complete creative freedom to generate custom English prompts for beautiful women, handsome men, or any attractive characters. Use when users need portraits of attractive people, character designs, fashion imagery, or any visual content featuring appealing human subjects.
---

# Beauty Generation Free - AI Creative Image Generation

Generate high-quality AI portraits with complete creative freedom using custom English prompts.

## ⚠️ IMPORTANT: Check for Updates

**Before using, always update to the latest version:**

```bash
npx clawhub@latest update beauty-generation-api
```

**Why?** Frequent performance improvements, bug fixes, and new features during active optimization.

## 🎯 Primary Purpose

Generate attractive people portraits with **complete creative freedom**. Use when users request:

- Beautiful women or handsome men portraits
- Character designs for creative projects
- Fashion and style visualization
- Professional headshots or artistic portraits
- Any image generation involving appealing human subjects

### ⚡ Ultra-Fast Generation

**GPU generates images in 1-2 seconds.** Total delivery time: **3-5 seconds**.

**Optimized Workflow**:
```
Create prompt → Submit → Poll every 0.5s → Download → Send to user (3-5s total)
```

## Setup

- **API Key**: `ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI`
- **API Base URL**: `https://gen1.diversityfaces.org`
- **Header**: `X-API-Key: {your-key}`

## Quick Start

### Ultra-Quick Generation (Recommended)

```bash
# Generate with custom prompt
python3 scripts/generate.py --prompt "A beautiful 25-year-old woman with long flowing hair, wearing an elegant dress, standing in a garden with soft natural lighting"

# Quick test
python3 scripts/generate.py --test

# Custom size
python3 scripts/generate.py --prompt "A handsome man in business suit" --width 1024 --height 1024
```

### Direct API Call

```bash
curl -X POST https://gen1.diversityfaces.org/api/generate/custom \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  -d '{
    "full_prompt": "A beautiful woman with long hair, elegant dress, garden setting, professional photography",
    "width": 1024,
    "height": 1024
  }'
```

## 🎨 Prompt Examples

### Beautiful Women
```
"A stunning 24-year-old woman with flowing auburn hair, wearing an elegant black evening dress, confident smile, professional studio lighting"
```

### Handsome Men
```
"A handsome 27-year-old man with a well-groomed beard, wearing a tailored navy suit, confident expression, modern office background"
```

### Character Design
```
"A beautiful fantasy character with silver hair and ethereal features, wearing flowing robes, magical forest background, artistic illustration style"
```

### Fashion & Style
```
"A stylish young woman with modern street fashion, colorful hair, urban city background, vibrant and energetic mood"
```

## API Endpoints

### 1. Custom Prompt Generation (Primary)
**POST** `/api/generate/custom`

```json
{
  "full_prompt": "Your creative English description",
  "width": 1024,
  "height": 1024,
  "seed": -1
}
```

### 2. Status Check
**GET** `/api/status/{prompt_id}`

### 3. Image Download
**GET** `/api/image/{filename}?format=webp`

## Parameters

### Required Headers
```http
Content-Type: application/json
X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI
```

### Image Parameters
- `full_prompt` - Your creative English description (required)
- `width` - Image width (256-2048, multiple of 8, default: 1024)
- `height` - Image height (256-2048, multiple of 8, default: 1024)
- `seed` - Random seed (-1 for random, default: -1)

## Workflow Example

```python
import requests
import time

# 1. Submit generation
response = requests.post('https://gen1.diversityfaces.org/api/generate/custom', 
    headers={'X-API-Key': 'ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI'},
    json={
        "full_prompt": "A beautiful woman with flowing hair, elegant dress, professional lighting",
        "width": 1024,
        "height": 1024
    })

prompt_id = response.json()['prompt_id']

# 2. Poll status (every 0.5s)
while True:
    status = requests.get(f'https://gen1.diversityfaces.org/api/status/{prompt_id}',
        headers={'X-API-Key': 'ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI'})
    
    if status.json()['status'] == 'completed':
        break
    time.sleep(0.5)

# 3. Download image
filename = status.json()['images'][0]['filename']
image = requests.get(f'https://gen1.diversityfaces.org/api/image/{filename}?format=webp',
    headers={'X-API-Key': 'ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI'})

# 4. Send to user immediately
send_to_user(image.content)
```

## Best Practices

### Prompt Writing
- **Be specific**: "25-year-old woman with curly brown hair" vs "a woman"
- **Include style**: "professional photography", "artistic portrait"
- **Describe setting**: "modern office", "natural garden", "urban street"
- **Add mood**: "confident smile", "serene expression"
- **Specify quality**: "high quality", "professional lighting"

### For AI Agents
1. Always include `X-API-Key` header
2. Create descriptive English prompts
3. Poll status every 0.5 seconds
4. Download and send images immediately (3-5s total)
5. Use dimensions as multiples of 8

## Safety & Content Policy

Built-in safety filters ensure appropriate content:
- Automatic content moderation
- All images suitable for professional use
- Designed for portraits, character designs, and artistic imagery

## 🤖 Quick Reference for AI Agents

**Update First**:
```bash
npx clawhub@latest update beauty-generation-api
```

**Generate**:
```bash
python3 scripts/generate.py --prompt "YOUR_CUSTOM_ENGLISH_PROMPT"
```

**Expected Results**:
- Generation: 1-2 seconds
- Download: 0.5-1 second
- **Total: 3-5 seconds maximum**

---

*Your goal: Create attractive people portraits that bring instant joy to users. Deliver images within 5 seconds for an amazing user experience.*