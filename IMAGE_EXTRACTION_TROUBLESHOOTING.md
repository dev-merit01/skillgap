# Image Extraction Troubleshooting

## Issue: "Extracted text is too short" or "Image quality too low"

When you upload an image (PNG, JPG, JPEG) for job descriptions or resumes, the system uses OpenAI Vision API to extract text. Sometimes the extraction returns too little text to analyze.

## Common Causes

1. **Low image quality** - Blurry, pixelated, or small text
2. **Poor contrast** - Light text on light background or vice versa
3. **Image too small** - Text too tiny to read
4. **Bad lighting** - Photos of documents with shadows or glare
5. **Scanned poorly** - Low resolution scan

## Solutions

### Option 1: Improve Your Image (Recommended for Images)

If you're uploading a photo or scan:

- **Take a clearer photo**
  - Use good lighting (daylight or bright indoor light)
  - Hold camera perpendicular to document
  - Ensure entire document is visible
  - Avoid shadows and glare
  - Use high resolution camera/phone

- **Rescan at higher quality**
  - Use 300+ DPI resolution
  - Ensure good contrast
  - Center the document

- **Crop and enhance** (before uploading)
  - Use an image editor to increase contrast
  - Crop to just the document area
  - Increase brightness if text is faint

### Option 2: Paste Text Manually (Fastest Solution)

Instead of uploading an image:

1. **Copy text from your job description**
   - From website, PDF, email, etc.
   - Paste directly into the text field

2. **This is faster and more accurate** because:
   - No OCR errors
   - All text is preserved exactly
   - No quality dependencies
   - Instant processing

### Option 3: Convert to PDF First

If you have an image document:

1. Use an online tool to convert image → PDF
   - Google Docs (upload image, download as PDF)
   - Online converters (convertio, ilovepdf, etc.)
2. Upload the PDF to the system
3. PDF text extraction is more reliable

## Why Manual Text Entry is Better

| Method | Speed | Accuracy | Quality Dependent |
|--------|-------|----------|-------------------|
| **Paste text** | ⚡ Instant | ✅ Perfect | ❌ No |
| **PDF upload** | 🔄 1-2 sec | ✅ Very good | ⚠️ Varies |
| **Image upload** | 🔄 2-5 sec | ⚠️ Variable | ⚠️ Yes |

## Technical Details

**Current extraction threshold**: 300 characters minimum

If your extraction returns less:
- For images: Usually indicates poor quality/contrast
- For PDFs: Usually indicates scanned documents or images embedded in PDF
- Solution: Paste text manually for best results

## Image Quality Tips

### Good Image For Extraction
✅ High contrast (dark text, white background)
✅ Sharp and clear text
✅ Well-lit photograph/scan
✅ Centered and straight
✅ No shadows or glare
✅ At least 200 DPI if scanned

### Poor Image For Extraction
❌ Faint or light text
❌ Blurry or pixelated
❌ Dark/colored background
❌ Tilted or rotated
❌ Shadows or glare visible
❌ Very small text
❌ Low DPI scan

## Recommended Workflow

1. **If you have text available** → Paste it manually (fastest)
2. **If you have a PDF** → Upload the PDF file
3. **If you have an image** → Improve it first using options above, then upload
4. **If extraction fails** → Paste the text manually instead

## Still Having Issues?

If image extraction continues to fail:
1. Check that OPENAI_API_KEY is properly configured
2. Verify the image file is actually PNG/JPG/JPEG
3. Try converting image to PDF first
4. Paste text manually as a reliable workaround

---

**Pro Tip**: For job descriptions, most have HTML/text available online - copy-paste is usually faster and more reliable than taking a screenshot!
