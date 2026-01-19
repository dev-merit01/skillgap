# OpenAI Vision API - Primary OCR Method

## Overview

The resume-job-match application now uses **OpenAI Vision API as the primary OCR method** for extracting text from uploaded image files (PNG, JPG, JPEG).

### Method Priority:
1. **PRIMARY**: OpenAI Vision API (gpt-4o-mini) - Cloud-based, most accurate
2. **FALLBACK**: Tesseract OCR (local, free) - Only if OpenAI not configured

## Why OpenAI as Primary?

- **Accuracy**: Handles scanned resumes, handwritten text, and poor quality images better
- **Robustness**: Works with various fonts, languages, and document layouts
- **Resume-Specific**: Uses optimized prompts for resume and job description extraction
- **Real-World Performance**: Better with actual resume images than local OCR engines

## Setup

### 1. Set Your OpenAI API Key

Choose one method:

**Option A: Environment Variable (Recommended)**
```bash
# Windows (Command Prompt)
set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# Windows (PowerShell)
$env:OPENAI_API_KEY='sk-xxxxxxxxxxxxxxxxxxxxx'

# Linux/Mac
export OPENAI_API_KEY='sk-xxxxxxxxxxxxxxxxxxxxx'
```

**Option B: Create `.env` file** in project root:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

**Option C: Update `settings.py` directly** (not recommended for production):
```python
OPENAI_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxx'
```

### 2. Restart Django Server

```bash
python manage.py runserver
```

Server will reload and use OpenAI Vision API for all image uploads.

## How It Works

When you upload an image (resume or job description):

1. **Image Validation**: File is checked (PNG/JPG/JPEG)
2. **Conversion**: Image is converted to base64 format
3. **OpenAI Vision Call**: Sent to gpt-4o-mini with context-specific prompt:
   - **Resume extraction prompt**: Optimized for CV structure (sections, dates, companies)
   - **Job description prompt**: Optimized for requirements and responsibilities
4. **Text Parsing**: Response is parsed and returned for analysis
5. **Fallback**: If OpenAI fails and Tesseract is installed, tries local OCR

## Available Configuration

In `resume_matcher/settings.py`:

```python
# OpenAI Configuration
OPENAI_API_KEY = env('OPENAI_API_KEY', default='')
OPENAI_API_BASE = env('OPENAI_API_BASE', default='https://api.openai.com/v1')
OPENAI_MODEL = env('OPENAI_MODEL', default='gpt-4o-mini')
```

## Error Handling

### If OpenAI API key is not set:
- Application will attempt Tesseract fallback (if installed)
- If neither method works: User gets clear error message with setup instructions

### If image extraction fails:
Clear error messages indicate:
- What methods were tried
- What's configured vs. not configured
- Recommended next steps

## Extraction Prompts

### Resume Extraction
```
Extract ALL text from this resume image exactly as written. 
Preserve all formatting including:
- Section headings (e.g., "EXPERIENCE", "EDUCATION", "SKILLS")
- Bullet points and dashes
- Line breaks and spacing
- Job titles, dates, company names
- All details exactly as they appear
```

### Job Description Extraction
```
Extract ALL text from this job description image exactly as it appears. 
Preserve the original formatting, including:
- Headings and section titles
- Bullet points and numbered lists
- Paragraph breaks
- All responsibilities and requirements
```

## Cost Considerations

Using gpt-4o-mini for vision:
- ~0.25 cents per image (1024x1024px typical resume)
- Batch of 100 resumes: ~$0.25
- Optional: Set `OPENAI_MODEL` to `gpt-4-turbo` for higher accuracy (more expensive)

## Verification

Test that OpenAI is working:

1. **Visit Debug Page**: `http://localhost:8000/debug/`
   - Should show: `"openai_api_key": "sk-...xxxxx"` (masked)
   - Should show: `"openai_model": "gpt-4o-mini"`

2. **Upload Test Image**:
   - Use a clear resume/job description image
   - Should complete extraction in 2-5 seconds
   - Check terminal for: `"Successfully extracted X chars from image via OpenAI"`

3. **Check Logs**:
   - Look for: `"Attempting image text extraction using OpenAI Vision API"`
   - Success: `"Successfully extracted X chars from image via OpenAI"`
   - Failure: `"OpenAI Vision extraction failed: ..."`

## Troubleshooting

### 401 Unauthorized / Invalid API Key
- Verify API key is correct and valid
- Check key hasn't reached usage limits
- Ensure no extra spaces in API key value

### 429 Too Many Requests
- Rate limit hit - wait before retrying
- Consider implementing queue for batch processing

### Image extraction returns empty text
- Try a clearer image
- Ensure good contrast and readability
- Check image isn't corrupted

### Still using Tesseract instead of OpenAI
- Verify `OPENAI_API_KEY` environment variable is set
- Restart Django server: `python manage.py runserver`
- Check `/debug/` page to confirm key is loaded

## Switching Between Methods

To switch from OpenAI back to Tesseract only:
```bash
# Clear API key (Tesseract will become primary if available)
unset OPENAI_API_KEY  # Linux/Mac
set OPENAI_API_KEY=  # Windows
```

To use both and control priority:
- Edit `ImageOCRExtractor.extract()` method in `analyzer/services/document_extractor.py`
- Reorder the try blocks to change priority

## Next Steps

- Configure your OPENAI_API_KEY environment variable
- Restart the Django server
- Upload a test resume or job description image
- Check that text extraction works in the application
