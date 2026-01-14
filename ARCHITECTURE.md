# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Single Page Application (Vanilla JS)                  │    │
│  │  - Firebase Authentication (Google Sign-In)            │    │
│  │  - Form Handling (Job Description + CV Upload)         │    │
│  │  - Results Display                                     │    │
│  └────────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTPS
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                     DJANGO APPLICATION                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Middleware Layer                                       │   │
│  │  - CSRF Protection                                      │   │
│  │  - Rate Limiting (IP/UID based)                         │   │
│  │  - Security Headers                                     │   │
│  └────────────────────────────────────────────────────────┘   │
│                            │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │  Views Layer (analyzer/views.py)                        │   │
│  │  - home(): Serve landing page                           │   │
│  │  - analyze(): Main CV analysis endpoint                 │   │
│  └────────────────────────────────────────────────────────┘   │
│                            │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │  Services Layer                                          │   │
│  │  ┌────────────────────────────────────────────────┐    │   │
│  │  │ Firebase Auth Service                          │    │   │
│  │  │ - verify_token()                               │    │   │
│  │  │ - Extract user info (uid, email)               │    │   │
│  │  └────────────────────────────────────────────────┘    │   │
│  │  ┌────────────────────────────────────────────────┐    │   │
│  │  │ CV Parser Service                              │    │   │
│  │  │ - parse_cv()                                   │    │   │
│  │  │ - extract_text_from_pdf() (pdfplumber)         │    │   │
│  │  │ - extract_text_from_docx() (python-docx)       │    │   │
│  │  │ *** ALL IN-MEMORY (BytesIO) ***                │    │   │
│  │  └────────────────────────────────────────────────┘    │   │
│  │  ┌────────────────────────────────────────────────┐    │   │
│  │  │ LLM Client Service                             │    │   │
│  │  │ - analyze()                                    │    │   │
│  │  │ - Structured prompting                         │    │   │
│  │  │ - JSON response parsing & validation           │    │   │
│  │  └────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬───────────────────────┬────────────────────────┘
                 │                       │
                 │                       │
         ┌───────▼──────┐       ┌───────▼──────────┐
         │   Firebase   │       │  OpenAI API      │
         │   Admin SDK  │       │  (or compatible) │
         │              │       │                  │
         │ - Token      │       │ - CV Analysis    │
         │   Validation │       │ - JSON Response  │
         └──────────────┘       └──────────────────┘
```

## Data Flow

### 1. Authentication Flow

```
User                 Browser              Django                Firebase
  │                     │                   │                     │
  │ Click Sign In       │                   │                     │
  ├────────────────────>│                   │                     │
  │                     │ signInWithPopup() │                     │
  │                     ├───────────────────────────────────────>│
  │                     │                   │   Verify Google     │
  │                     │<──────────────────────────────────────┤
  │                     │ ID Token          │                     │
  │                     │                   │                     │
  │ Store Token         │                   │                     │
  ├─────────────────────┤                   │                     │
```

### 2. Analysis Request Flow

```
Browser              Django              CV Parser         LLM API
  │                     │                     │                │
  │ POST /analyze/      │                     │                │
  │ Bearer <token>      │                     │                │
  │ job_description     │                     │                │
  │ cv_file (bytes)     │                     │                │
  ├────────────────────>│                     │                │
  │                     │ Verify Token        │                │
  │                     ├─────────────────────>Firebase         │
  │                     │<────────────────────┤                │
  │                     │ Valid (uid, email)  │                │
  │                     │                     │                │
  │                     │ parse_cv()          │                │
  │                     ├────────────────────>│                │
  │                     │ BytesIO → Text      │                │
  │                     │<───────────────────┤                │
  │                     │                     │                │
  │                     │ analyze(cv, job)    │                │
  │                     ├────────────────────────────────────>│
  │                     │                     │ System Prompt  │
  │                     │                     │ + User Content │
  │                     │<───────────────────────────────────┤
  │                     │ JSON Response       │                │
  │                     │ {match_score, ...}  │                │
  │<────────────────────┤                     │                │
  │ Display Results     │                     │                │
  │                     │                     │                │
  │ [Data Discarded]    │ [Memory Freed]      │                │
```

## Key Design Principles

### 1. **Stateless Architecture**
- No user sessions beyond authentication
- Each request is self-contained
- No server-side state between requests

### 2. **Zero Persistence**
- CVs never touch disk: `BytesIO` → Parse → Analyze → Discard
- Job descriptions never stored
- Only Django sessions in database (not user data)

### 3. **In-Memory Processing**
```python
# Typical flow
file_bytes = request.FILES['cv_file'].read()  # ← bytes in RAM
pdf_stream = BytesIO(file_bytes)              # ← in-memory file
with pdfplumber.open(pdf_stream) as pdf:      # ← parse from RAM
    text = extract_text(pdf)
# After function returns, all objects garbage collected
```

### 4. **Security Layers**

```
Request → Rate Limit Check → CSRF Check → Auth Verification → Input Validation → Processing
```

## Component Responsibilities

| Component | Responsibility | No Side Effects |
|-----------|---------------|-----------------|
| `views.py` | Request routing, orchestration | ✓ Stateless |
| `firebase_auth.py` | Token verification | ✓ No writes |
| `cv_parser.py` | File → Text (in-memory) | ✓ No disk I/O |
| `llm_client.py` | Text → Analysis | ✓ No storage |
| `middleware.py` | Rate limiting, security | ✗ Tracks in-memory only |

## Scalability Considerations

### Horizontal Scaling
- **Stateless design** enables multiple instances
- No shared session state required
- Rate limiting uses in-memory store (consider Redis for multi-server)

### Performance Bottlenecks
1. **LLM API calls**: 2-10s per request
   - Solution: Set realistic user expectations
   - Consider batch processing for bulk use
2. **File parsing**: 100ms - 1s for large files
   - Solution: Client-side file size limits
3. **Rate limiting**: In-memory dict grows over time
   - Solution: Periodic cleanup (built-in) or use Redis

### Cost Optimization
- **LLM API**: Primary cost driver
  - Use smaller models (`gpt-4o-mini` vs `gpt-4`)
  - Implement token limits
  - Cache common patterns (optional)
- **Compute**: Minimal (no heavy processing)
- **Storage**: Near-zero (no file storage)

## Deployment Topologies

### Single Server
```
Nginx (SSL, static) → Gunicorn (Django) → Firebase + OpenAI
```

### Multi-Server (Load Balanced)
```
Load Balancer
    ├─> Server 1 (Gunicorn)
    ├─> Server 2 (Gunicorn)  ─→ Redis (rate limiting)
    └─> Server 3 (Gunicorn)
            ↓
    Firebase + OpenAI
```

### Serverless (e.g., Cloud Run)
```
Cloud Run (auto-scale) → Firebase + OpenAI
- No persistent connections
- Perfect for stateless architecture
- Pay-per-request model
```

## Security Architecture

```
┌─────────────────────────────────────────────┐
│  Security Layers                            │
├─────────────────────────────────────────────┤
│  1. HTTPS/TLS (Transport)                   │
│  2. Firebase Token Verification (Identity)  │
│  3. Rate Limiting (Abuse Prevention)        │
│  4. CSRF Protection (Request Forgery)       │
│  5. Input Validation (Malicious Data)       │
│  6. File Type Enforcement (Upload Security) │
│  7. Content-Type Validation (Headers)       │
└─────────────────────────────────────────────┘
```

## Technology Choices Rationale

| Technology | Why Chosen | Alternatives Considered |
|------------|-----------|------------------------|
| **Django** | Full-featured, secure defaults, excellent docs | FastAPI (less features), Flask (more boilerplate) |
| **Firebase Auth** | Managed auth, no password handling, easy Google sign-in | Auth0 (more expensive), Django Auth (complex) |
| **OpenAI API** | Best-in-class LLM, structured outputs, reliable | Anthropic (good but newer), Local LLMs (resource intensive) |
| **pdfplumber** | Excellent text extraction, handles complex PDFs | PyPDF2 (less robust), PDFMiner (more complex) |
| **python-docx** | Standard for DOCX parsing, simple API | python-office (overkill) |
| **Vanilla JS** | No build step, simple, fast | React (overkill), Vue (unnecessary complexity) |

## Future Enhancement Opportunities

1. **Redis Integration**: Distributed rate limiting
2. **Result Caching**: Cache anonymous analyses (optional)
3. **Batch Processing**: Handle multiple CVs at once
4. **WebSockets**: Real-time progress updates
5. **Analytics**: Anonymous usage statistics
6. **Multi-Language**: i18n support
7. **Custom Models**: Fine-tuned LLM for specific industries

---

**Architecture Version:** 1.0  
**Last Updated:** January 2026  
**Review Cycle:** Quarterly
