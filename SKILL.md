---
name: beauty-generation-api
description: Professional AI beauty image generation service supporting 140+ nationalities. Generate high-quality portraits of women with customizable parameters including style, age, nationality, clothing, scene, and mood. CRITICAL - All parameters must be in Chinese format (e.g., "清纯", "中国", "连衣裙") as the API has strict validation. Use when user needs to create beautiful female portraits, character designs, or artistic images with specific aesthetic requirements (e.g., "generate a 22-year-old Japanese woman in traditional kimono", "create a modern Chinese businesswoman portrait", "design a vintage-style European model").
---

# Beauty Generation API

Generate high-quality AI portraits of beautiful women using advanced ComfyUI models with extensive customization options.

## 🚨 CRITICAL: Chinese Format Requirements

**MANDATORY**: All parameters MUST be in Chinese format. The API has strict validation and will reject requests with incorrect formats.

### ⚠️ Format Validation Rules
- **Style**: Must use Chinese terms like `清纯`, `性感`, `古典` - NOT English like "pure", "sexy", "classic"
- **Nationality**: Must use Chinese country names like `中国`, `日本`, `美国` - NOT English like "China", "Japan", "USA"  
- **Clothing**: Must use Chinese terms like `连衣裙`, `旗袍`, `西装` - NOT English like "dress", "qipao", "suit"
- **Scene**: Must use Chinese terms like `室内`, `户外`, `咖啡厅` - NOT English like "indoor", "outdoor", "cafe"
- **Mood**: Must use Chinese terms like `甜美`, `优雅`, `活泼` - NOT English like "sweet", "elegant", "lively"

### 🔥 Common Validation Errors
```json
{
  "success": false,
  "error": "参数验证失败",
  "details": [
    "无效的风格参数: pure (应使用: 清纯)",
    "无效的国籍参数: China (应使用: 中国)",
    "无效的服饰参数: dress (应使用: 连衣裙)"
  ]
}
```

### ✅ Correct Format Examples
```json
{
  "style": "清纯",        // ✅ Correct Chinese
  "nationality": "中国",   // ✅ Correct Chinese  
  "clothing": "连衣裙",    // ✅ Correct Chinese
  "scene": "咖啡厅",      // ✅ Correct Chinese
  "mood": "甜美"          // ✅ Correct Chinese
}
```

### ❌ Incorrect Format Examples  
```json
{
  "style": "pure",        // ❌ Will be REJECTED
  "nationality": "China", // ❌ Will be REJECTED
  "clothing": "dress",    // ❌ Will be REJECTED
  "scene": "cafe",        // ❌ Will be REJECTED
  "mood": "sweet"         // ❌ Will be REJECTED
}
```

**IMPORTANT**: Always use the `/api/presets` endpoint to get the exact Chinese terms accepted by the API. Do not guess or translate - use only the provided Chinese values.

## Setup

- Needs API Key: `ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI`
- API Base URL: `https://gen1.diversityfaces.org`
- All requests require `X-API-Key` header for authentication

## Quick Start

Generate a standard beauty portrait:

```bash
curl -X POST https://gen1.diversityfaces.org/api/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  -d '{
    "style": "清纯",
    "age": "22",
    "nationality": "中国",
    "clothing": "连衣裙",
    "scene": "室内",
    "mood": "甜美"
  }'
```

Generate random beauty with specific overrides:

```bash
curl -X POST https://gen1.diversityfaces.org/api/generate/random \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  -d '{
    "clothing": "旗袍",
    "nationality": "中国"
  }'
```

## Style Library

### Beauty Styles (风格)
- `清纯` - Pure and innocent look with natural beauty
- `性感` - Elegant and alluring with sophisticated charm  
- `古典` - Classical traditional beauty with timeless appeal
- `现代` - Modern contemporary style with trendy aesthetics
- `甜美` - Sweet and cute with youthful charm
- `冷艳` - Cool and aloof with mysterious elegance
- `知性` - Intellectual and refined with scholarly grace
- `活泼` - Lively and energetic with vibrant personality

### Nationalities (国籍) - 140+ Countries Supported
**East Asian**: 中国, 日本, 韩国, 朝鲜, 蒙古, 台湾, 香港, 澳门
**Southeast Asian**: 新加坡, 泰国, 越南, 马来西亚, 印度尼西亚, 菲律宾, 缅甸, 柬埔寨, 老挝, 文莱, 东帝汶
**South Asian**: 印度, 巴基斯坦, 孟加拉国, 斯里兰卡, 尼泊尔, 不丹, 马尔代夫, 阿富汗
**Central Asian**: 俄罗斯, 哈萨克斯坦, 乌兹别克斯坦, 土库曼斯坦, 塔吉克斯坦, 吉尔吉斯斯坦, 阿塞拜疆, 亚美尼亚, 格鲁吉亚
**Middle East**: 土耳其, 伊朗, 伊拉克, 叙利亚, 黎巴嫩, 约旦, 以色列, 巴勒斯坦, 沙特阿拉伯, 阿联酋, 卡塔尔, 科威特, 巴林, 阿曼, 也门
**Africa**: 埃及, 利比亚, 突尼斯, 阿尔及利亚, 摩洛哥, 苏丹, 埃塞俄比亚, 肯尼亚, 坦桑尼亚, 乌干达, 卢旺达, 南非, 尼日利亚, 加纳, 塞内加尔, 马里, 布基纳法索, 象牙海岸, 喀麦隆, 刚果, 安哥拉, 赞比亚, 津巴布韦, 博茨瓦纳, 纳米比亚, 马达加斯加, 毛里求斯, 塞舌尔
**North America**: 美国, 加拿大, 墨西哥, 古巴, 牙买加, 海地, 多米尼加, 波多黎各, 特立尼达和多巴哥, 巴巴多斯, 巴哈马
**South America**: 巴西, 阿根廷, 智利, 秘鲁, 哥伦比亚, 委内瑞拉, 厄瓜多尔, 玻利维亚, 巴拉圭, 乌拉圭, 圭亚那, 苏里南
**Europe**: 英国, 法国, 德国, 意大利, 西班牙, 葡萄牙, 荷兰, 比利时, 瑞士, 奥地利, 瑞典, 挪威, 丹麦, 芬兰, 冰岛, 爱尔兰, 波兰, 捷克, 斯洛伐克, 匈牙利, 罗马尼亚, 保加利亚, 希腊, 塞尔维亚, 克罗地亚, 斯洛文尼亚, 波斯尼亚, 黑山, 北马其顿, 阿尔巴尼亚, 摩尔多瓦, 乌克兰, 白俄罗斯, 立陶宛, 拉脱维亚, 爱沙尼亚, 马耳他, 塞浦路斯, 卢森堡, 摩纳哥, 安道尔, 圣马力诺, 梵蒂冈
**Oceania**: 澳大利亚, 新西兰, 斐济, 巴布亚新几内亚, 瓦努阿图, 所罗门群岛, 萨摩亚, 汤加, 帕劳, 密克罗尼西亚, 马绍尔群岛, 基里巴斯, 图瓦卢, 瑙鲁

### Clothing Styles (服饰)
**Traditional**: 旗袍, 和服, 韩服, 中山装, 民族服装
**Modern**: 连衣裙, 衬衫, T恤, 毛衣, 西装, 外套
**Casual**: 牛仔裤, 卫衣, 休闲装, 运动装
**Formal**: 晚礼服, 正装, 商务装
**Vintage**: 复古装, 古典装

### Scenes (场景)
**Indoor**: 室内, 咖啡厅, 图书馆, 酒店, 餐厅, 办公室, 学校
**Outdoor**: 户外, 花园, 阳台, 森林, 公园, 广场, 桥梁
**Urban**: 城市, 商场, 机场, 火车站, 地铁
**Natural**: 海边, 沙滩, 山顶, 湖边

### Moods (情绪)
**Gentle**: 甜美, 温柔, 纯真, 害羞, 温暖
**Confident**: 优雅, 高贵, 自信, 知性, 严肃
**Playful**: 活泼, 俏皮, 调皮, 可爱, 开朗
**Mysterious**: 神秘, 冷艳, 妩媚, 忧郁, 慵懒

## API Endpoints

### 1. Standard Generation
**POST** `/api/generate`

Generate with specific parameters:
```json
{
  "style": "清纯",
  "age": "22",
  "nationality": "日本", 
  "scene": "户外",
  "mood": "甜美",
  "hair_style": "长发",
  "hair_color": "黑色",
  "skin_tone": "白皙",
  "clothing": "连衣裙",
  "clothing_color": "白色",
  "clothing_style": "优雅",
  "accessories": "项链",
  "width": 1024,
  "height": 1024,
  "steps": 4,
  "seed": -1
}
```

### 2. Random Generation
**POST** `/api/generate/random`

Generate with random parameters (can override specific ones):
```json
{
  "clothing": "旗袍",
  "nationality": "中国",
  "width": 1024,
  "height": 1024
}
```

### 3. Custom Prompt Generation
**POST** `/api/generate/custom`

Use custom text prompts:
```json
{
  "full_prompt": "一位优雅的25岁中国女性，穿着白色旗袍，在古典园林中微笑，高质量摄影，胶片质感",
  "width": 1024,
  "height": 1024,
  "steps": 4
}
```

### 4. Status Check
**GET** `/api/status/{prompt_id}`

Check generation progress:
```bash
curl -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  https://gen1.diversityfaces.org/api/status/abc123
```

### 5. Image Download
**GET** `/api/image/{filename}`

Download generated images with format options:
```bash
curl -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  "https://gen1.diversityfaces.org/api/image/beauty-uuid.png?format=webp" \
  -o beauty.webp
```

### 6. Get Presets
**GET** `/api/presets`

Get all available parameter options:
```bash
curl -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  https://gen1.diversityfaces.org/api/presets
```

## Parameters Reference

### Required Headers
```http
Content-Type: application/json
X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI
```

### Image Parameters
- `width` - Image width (256-2048, must be multiple of 8)
- `height` - Image height (256-2048, must be multiple of 8)  
- `steps` - Sampling steps (1-20, default: 4)
- `seed` - Random seed (-1 for random, 0-2147483647)

### Style Parameters
- `style` - Beauty style (清纯, 性感, 古典, 现代, etc.)
- `age` - Age in years (18-28)
- `nationality` - Country/ethnicity
- `scene` - Background setting
- `mood` - Emotional expression
- `hair_style` - Hairstyle (长发, 短发, 马尾辫, etc.)
- `hair_color` - Hair color (黑色, 棕色, 金色, etc.)
- `skin_tone` - Skin tone (白皙, 健康色, 小麦色, etc.)
- `clothing` - Clothing type (连衣裙, 旗袍, 衬衫, etc.)
- `clothing_color` - Clothing color
- `clothing_style` - Clothing style (优雅, 休闲, 正式, etc.)
- `accessories` - Accessories (项链, 耳环, 手镯, etc.)

## Workflow Examples

### Portrait Photography Session
```bash
# Generate professional headshots
curl -X POST https://gen1.diversityfaces.org/api/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  -d '{
    "style": "知性",
    "age": "25", 
    "nationality": "中国",
    "clothing": "西装",
    "clothing_color": "黑色",
    "scene": "办公室",
    "mood": "自信",
    "width": 1024,
    "height": 1024
  }'
```

### Fashion Design Concepts
```bash
# Generate fashion model concepts
curl -X POST https://gen1.diversityfaces.org/api/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  -d '{
    "style": "现代",
    "age": "20",
    "nationality": "韩国", 
    "clothing": "晚礼服",
    "clothing_color": "红色",
    "scene": "城市",
    "mood": "优雅",
    "width": 1024,
    "height": 1024
  }'
```

### Cultural Character Design
```bash
# Generate traditional cultural portraits
curl -X POST https://gen1.diversityfaces.org/api/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  -d '{
    "style": "古典",
    "age": "23",
    "nationality": "日本",
    "clothing": "和服", 
    "clothing_color": "粉色",
    "scene": "花园",
    "mood": "温柔",
    "accessories": "发饰",
    "width": 1024,
    "height": 1024
  }'
```

## Error Handling

### Authentication Errors
```json
{
  "success": false,
  "error": "API密钥验证失败",
  "code": "INVALID_API_KEY"
}
```

### Parameter Validation Errors
```json
{
  "success": false,
  "error": "参数验证失败",
  "details": ["无效的风格参数: 不存在的风格"],
  "valid_presets": {
    "styles": ["清纯", "性感", "古典", "现代"]
  }
}
```

### Safety Check Errors
```json
{
  "success": false,
  "error": "安全检查失败", 
  "details": "检测到不当内容关键词",
  "code": "SECURITY_VIOLATION"
}
```

## Best Practices

### For AI Agents
1. **Always include authentication**: Add `X-API-Key` header to all requests
2. **Use appropriate parameters**: Choose culturally appropriate combinations
3. **Handle async workflow**: Submit → Poll status → Download images
4. **Respect rate limits**: Add delays between requests if needed
5. **Validate parameters**: Use `/api/presets` to get valid options

### Parameter Combinations
- **Professional portraits**: `style="知性"`, `clothing="西装"`, `scene="办公室"`
- **Traditional beauty**: `style="古典"`, `clothing="旗袍"`, `nationality="中国"`
- **Modern fashion**: `style="现代"`, `clothing="连衣裙"`, `scene="城市"`
- **Casual lifestyle**: `style="活泼"`, `clothing="休闲装"`, `scene="咖啡厅"`

### Image Quality Tips
- Use `steps=4` for fast generation, `steps=8-12` for higher quality
- Recommended sizes: 1024x1024 (square), 1024x1536 (portrait), 1536x1024 (landscape)
- Use `format=webp` for smaller file sizes, `format=png` for highest quality

## Safety & Content Policy

This API includes built-in safety filters to ensure appropriate content:
- Automatic safety prompts added to all generations
- Sensitive keyword detection and filtering
- Strict content moderation for all outputs
- All generated images are appropriate for professional use

The service is designed for creating professional portraits, character designs, fashion concepts, and artistic imagery while maintaining high ethical standards.