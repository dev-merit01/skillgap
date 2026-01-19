# Quick Start: Enable Image Text Extraction with OpenAI

## What You Need

To extract text from images (PNG, JPG, JPEG) when uploading job descriptions, you need one of these:

1. **OpenAI API Key** (Recommended - cloud-based, higher accuracy)
2. **Tesseract OCR** (Free, local installation)

---

## Option 1: OpenAI API (Recommended)

### Step 1: Get Your API Key

1. Visit https://platform.openai.com/api-keys
2. Sign in (create account if needed)
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-`)

### Step 2: Add to Your Project

**Method A: Environment Variable (Quick Test)**

Windows Command Prompt:
```cmd
set OPENAI_API_KEY=sk-your-key-here
python manage.py runserver
```

Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
python manage.py runserver
```

macOS/Linux:
```bash
export OPENAI_API_KEY="sk-your-key-here"
python manage.py runserver
```

**Method B: .env File (Recommended)**

Create `.env` file in project root:
```
OPENAI_API_KEY=sk-your-key-here
```

Then restart the server - it will automatically load from .env

### Step 3: Test It

1. Open http://localhost:8000/debug/
2. Check that `openai_api_key` shows `true`
3. Try uploading an image - it should work now!

### Cost

- **Free tier:** $5 credit for new accounts
- **Pay-as-you-go:** ~$0.01 per image with gpt-4o-mini
- You can set usage limits in your OpenAI dashboard

---

## Option 2: Tesseract OCR (Free, Local)

### Installation

**Windows:**
1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (use default path)
3. Restart server

**macOS:**
```bash
brew install tesseract
python manage.py runserver
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
python manage.py runserver
```

### Benefits
- ✅ Free
- ✅ No API key needed
- ✅ Works offline
- ✅ Fast for simple images

### Limitations
- ❌ Lower accuracy than OpenAI for complex documents
- ❌ Requires local installation

---

## How It Works

When you upload an image, the system tries in this order:

1. **Tesseract OCR** (if installed) - Fast, local, free
2. **OpenAI Vision API** (if API key set) - Accurate, cloud-based
3. **Manual text entry** - Paste text as fallback

If both fail or neither is available, you can paste the job description text manually.

---

## Troubleshooting

### "Could not extract text from this image"

**Check what's available:**
- Visit http://localhost:8000/debug/
- Look for `openai_api_key` value

**If both Tesseract and OpenAI unavailable:**
```
Error: No OCR methods are configured.
Solution: Install Tesseract OR set OpenAI API key
```

**If Tesseract available but OpenAI not:**
```
Error: Tesseract failed, and OpenAI API not configured
Solution: Try a clearer image OR set OpenAI API key
```

### Tesseract command not found
- Windows: Reinstall Tesseract (check it's in PATH)
- macOS: Run `brew reinstall tesseract`
- Linux: Run `sudo apt-get install tesseract-ocr`

### OpenAI API error
- Check API key is correct
- Verify you have credits (check https://platform.openai.com/account/billing/overview)
- Check your account isn't rate limited

---

## Next Steps

1. Choose Option 1 (OpenAI) or Option 2 (Tesseract)
2. Follow the installation steps above
3. Restart the server
4. Try uploading an image
5. It should now extract text successfully!

For more details, see [OPENAI_SETUP.md](OPENAI_SETUP.md)
