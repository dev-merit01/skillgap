# How to Enable OpenAI Image Text Extraction

## Step 1: Get an OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in with your OpenAI account (create one if needed)
3. Click "Create new secret key"
4. Copy the key (it will start with `sk-`)
5. **IMPORTANT:** Save it in a safe place - you won't be able to see it again

## Step 2: Set the API Key

### Option A: Using Environment Variable (Development)

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
python manage.py runserver
```

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-api-key-here"
python manage.py runserver
```

**On macOS/Linux (Bash):**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
python manage.py runserver
```

### Option B: Using .env File (Recommended)

1. Create a `.env` file in the project root directory:
```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
DEBUG=True
```

2. The application will automatically read from this file (using python-decouple)
3. Restart the server: `python manage.py runserver`

## Step 3: Verify It's Working

1. Go to http://localhost:8000/debug/
2. Check that `openai_api_key` shows `true`
3. Try uploading an image again

## Pricing Information

- OpenAI Vision API typically costs around **$0.01 per image** for gpt-4o-mini
- Free trial includes $5 in credits
- You can set usage limits in your OpenAI account dashboard

## Fallback Option: Local OCR

If you don't have an OpenAI API key, the system will try to use **Tesseract OCR** (free, local):

1. **On Windows:** Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
2. **On macOS:** `brew install tesseract`
3. **On Linux:** `sudo apt-get install tesseract-ocr`

After installation, restart the server and image text extraction will work locally without any API key.

## Troubleshooting

### "Image text extraction not configured"
- OpenAI API key is not set
- Check that your .env file is in the project root directory
- Restart the server after setting the environment variable

### "Failed to process image due to API error"
- Your OpenAI API key may be invalid or expired
- Check that you have credits available in your OpenAI account
- Verify the API key by visiting https://platform.openai.com/api-keys

### "Could not extract text from this image"
- The image may be too low quality or contain no readable text
- Try a clearer image or paste the text manually
- Make sure the image is PNG, JPG, or JPEG format
