# Quick Start: OpenAI Vision API for Image OCR

## TL;DR Setup (5 minutes)

### 1. Get Your OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create a new API key
- Copy the key (starts with `sk-`)

### 2. Set Environment Variable

**Windows Command Prompt:**
```bash
set OPENAI_API_KEY=sk-YOUR_KEY_HERE
python manage.py runserver
```

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY='sk-YOUR_KEY_HERE'
python manage.py runserver
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY='sk-YOUR_KEY_HERE'
python manage.py runserver
```

### 3. Test It Works
1. Visit http://localhost:8000/debug/ - Should show your API key (masked)
2. Upload a resume or job description image
3. Text should extract in 2-5 seconds

## What Changed

✅ OpenAI Vision API is now **PRIMARY** method (not fallback)
✅ Tesseract is now **FALLBACK** (only if OpenAI fails or key not set)
✅ Resume-specific extraction prompt added
✅ Job description-specific extraction prompt added
✅ Better error messages showing what's configured

## Architecture

```
Image Upload
    ↓
    Try OpenAI Vision (gpt-4o-mini) ← PRIMARY
        Success? → Return text
        Fail? ↓
    Try Tesseract OCR ← FALLBACK
        Success? → Return text
        Fail? ↓
    Return error with setup instructions
```

## Extraction Prompts

The system uses optimized prompts for different document types:

**Resume** (optimized for CV structure):
- Preserves section headings, dates, company names
- Keeps all formatting and bullet points
- Exact reproduction of original text

**Job Description** (optimized for requirements/responsibilities):
- Preserves headings and lists
- Maintains paragraph structure
- Captures all details exactly

## Cost

- ~$0.0025 per image (using gpt-4o-mini)
- 100 resumes = ~$0.25
- Track usage at https://platform.openai.com/account/usage

## Troubleshooting

### "Image text extraction not configured"
→ Set OPENAI_API_KEY and restart server

### "401 Unauthorized"
→ Check API key is correct and valid

### "No text extracted"
→ Try a clearer, higher contrast image

### Still using Tesseract
→ Verify OPENAI_API_KEY is set and restart Django
→ Check /debug/ page to confirm key is loaded

## Files Modified

- `analyzer/services/document_extractor.py` - Reordered priority, added prompts
- `resume_matcher/settings.py` - Already configured for OpenAI
- Documentation created:
  - `OPENAI_VISION_PRIMARY.md` - Full setup guide
  - `OPENAI_VISION_IMPLEMENTATION.md` - Technical details

## Next Steps

1. ✅ Set OPENAI_API_KEY environment variable
2. ✅ Restart Django server
3. ✅ Upload a test image to verify
4. ✅ Check terminal logs: "Successfully extracted X chars from image via OpenAI"

---

Need more details? See `OPENAI_VISION_PRIMARY.md`
