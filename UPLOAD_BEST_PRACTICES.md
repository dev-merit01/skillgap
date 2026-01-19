# Best Practices: Uploading Job Descriptions & Resumes

## Quick Reference

| File Type | Quality | Speed | Recommendation |
|-----------|---------|-------|-----------------|
| Text (Pasted) | ✅ Perfect | ⚡ Instant | **Best** |
| PDF | ✅ Excellent | 🔄 2-3 sec | **Good** |
| DOCX | ✅ Excellent | 🔄 2-3 sec | **Good** |
| Image (High Quality) | ⚠️ Variable | 🔄 3-5 sec | Use only if needed |

## Job Description - Best Approach

### Method 1: Copy-Paste Text (Recommended ⭐⭐⭐)
```
1. Find job description on website/email
2. Select and copy all the text
3. Paste into text field
4. Click Analyze
✅ Instant results, 100% accuracy
```

### Method 2: Upload PDF (Good ⭐⭐)
```
1. Have job posting as PDF file
2. Upload to system
3. Review extracted text
4. Click Analyze
✅ Usually works well, 2-3 seconds
```

### Method 3: Upload Image (Last Resort ⭐)
```
1. Take screenshot/photo of job posting
2. Upload image file (PNG/JPG)
3. Check if text extracted properly
4. If too short/unclear, paste text manually instead
⚠️ Quality dependent, 3-5 seconds
```

## Resume - Best Approach

### Method 1: Upload PDF (Recommended ⭐⭐⭐)
```
1. Export/save resume as PDF
2. Upload PDF file
3. Click Analyze
✅ Fastest for resumes, usually perfect extraction
```

### Method 2: Upload DOCX (Good ⭐⭐)
```
1. Have resume as Word document
2. Upload DOCX file
3. Click Analyze
✅ Also works well, instant parsing
```

### Method 3: Take Screenshot/Image (Last Resort ⭐)
```
1. Take photo of printed resume or screenshot
2. Upload as PNG/JPG
3. If extraction fails, provide PDF/DOCX instead
⚠️ Only for when digital files unavailable
```

## Troubleshooting by Symptom

### "Text too short" Error

**If uploading an image:**
- The image quality is likely the issue
- Solution: Use clearer image, PDF, or paste text manually

**If uploading a PDF:**
- PDF might be image-based (scanned document)
- Solution: Try copy-pasting text from PDF viewer, or use OCR tool first

**If pasting text:**
- Job description might actually be very short
- Solution: Provide full job description

### "File not recognized" Error

- File format not supported (only PDF, DOCX, PNG, JPG, JPEG)
- Solution: Convert to supported format first

### "OCR extraction failed" for Images

- OpenAI API key not configured
- Image quality too poor
- Solution: 
  1. Verify OPENAI_API_KEY is set
  2. Try clearer image or paste text
  3. Use PDF/DOCX if available

## Tips for Best Results

### For Job Descriptions
✅ **Do**:
- Copy text from job posting website
- Use full job description (all requirements/responsibilities)
- Include company info and role title
- Paste text directly for best matching

❌ **Don't**:
- Use just the job title
- Upload as image unless necessary
- Use outdated job postings
- Truncate or edit requirements

### For Resumes
✅ **Do**:
- Use PDF format (most compatible)
- Include all relevant experience
- Use actual resume file (not screenshot)
- Update resume before analysis

❌ **Don't**:
- Use resume image/screenshot if PDF available
- Strip out important details
- Use heavily formatted/design-heavy resumes
- Submit incomplete resumes

## File Size Limits

- **Maximum file size**: 2 MB
- **Maximum job description**: 50,000 characters (~10,000 words)
- **Recommended sizes**:
  - Job description: 500-5,000 characters
  - Resume: any length (typically 2,000-10,000 chars)

## Supported File Types

| Format | Support | Notes |
|--------|---------|-------|
| PDF | ✅ Yes | Best for resumes |
| DOCX | ✅ Yes | Word documents |
| PNG | ✅ Yes | Image format |
| JPG | ✅ Yes | Image format |
| JPEG | ✅ Yes | Image format |
| TXT | ❌ No | Not supported, paste to text field instead |
| DOC | ❌ No | Use DOCX (save as .docx) |

## Performance

### Expected Processing Times
- **Text paste**: < 1 second
- **PDF/DOCX upload**: 2-3 seconds
- **Image upload**: 3-5 seconds
- **LLM analysis**: 5-10 seconds

### If Processing Takes Longer
- Check internet connection
- Verify file size < 2 MB
- Try again (servers may be busy)
- Use text paste method (faster)

## Getting Best Match Results

1. **Use complete documents**
   - Full job description (not just snippet)
   - Full resume (not just highlights)

2. **Use current information**
   - Recent job posting (within 30 days)
   - Updated resume (last 6 months)

3. **Ensure text quality**
   - Clear, readable text
   - No OCR errors if from image
   - Proper formatting preserved

4. **Provide context**
   - Include company name if available
   - Include job level/seniority
   - Include any special requirements

## Example Workflows

### Workflow 1: Online Job Posting
```
1. Find job on LinkedIn/Indeed/etc
2. Select all text (Ctrl+A or highlight)
3. Copy (Ctrl+C)
4. Paste into job description field
5. Upload your resume PDF
6. Click Analyze
Result: ✅ Instant, accurate matching
```

### Workflow 2: PDF Job Description
```
1. Have job posting PDF
2. Copy text from PDF viewer
3. Paste into text field
4. Upload resume
5. Click Analyze
Result: ✅ Fast, reliable
```

### Workflow 3: Job Description Image
```
1. Screenshot/photo of job posting
2. Upload image
3. If extraction < 300 chars: paste text manually
4. Upload resume
5. Click Analyze
Result: ⚠️ Works if image quality good
```

---

**Remember**: The simpler the workflow (text paste > PDF upload > Image upload), the faster and more reliable your results!
