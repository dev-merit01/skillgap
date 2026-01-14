# 🔒 Security Checklist for AI Job Matcher

## Pre-Deployment Security Audit

### ✅ Environment & Configuration

- [ ] `DEBUG=False` in production `.env`
- [ ] Strong `DJANGO_SECRET_KEY` (50+ random characters)
- [ ] `ALLOWED_HOSTS` restricted to actual domain names
- [ ] All sensitive credentials in `.env` (not in code)
- [ ] `.env` file added to `.gitignore`
- [ ] Firebase service account JSON not committed to git
- [ ] HTTPS enabled (SSL/TLS certificates configured)
- [ ] `SECURE_SSL_REDIRECT=True` in production

### ✅ Firebase Security

- [ ] Firebase Authentication enabled
- [ ] Google sign-in method properly configured
- [ ] Firebase service account has minimal required permissions
- [ ] Firebase credentials file has restricted read permissions (chmod 600)
- [ ] Firebase Web API key restrictions configured in console
- [ ] Authorized domains configured in Firebase Console

### ✅ API Security

- [ ] OpenAI API key has usage limits configured
- [ ] API key stored securely in environment variables
- [ ] API rate limiting enabled in settings
- [ ] Token verification enabled for all protected endpoints
- [ ] CSRF protection enabled (Django default)

### ✅ Input Validation

- [ ] File size limits enforced (MAX_UPLOAD_SIZE)
- [ ] File type restrictions enforced (.pdf, .docx only)
- [ ] Job description length limited
- [ ] File content validation (not just extension checking)
- [ ] Malicious file upload prevention

### ✅ Rate Limiting & Abuse Prevention

- [ ] Rate limiting middleware enabled
- [ ] Appropriate rate limits configured per user/IP
- [ ] Rate limit window configured appropriately
- [ ] Failed authentication attempts logged
- [ ] Suspicious activity monitoring in place

### ✅ Data Privacy

- [ ] Confirmed: No CVs stored in database
- [ ] Confirmed: No job descriptions stored in database
- [ ] Confirmed: Files processed in-memory only
- [ ] File upload handling uses BytesIO (not disk writes)
- [ ] No sensitive data in application logs
- [ ] Privacy policy displayed to users

### ✅ HTTP Security Headers

- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options: nosniff
- [ ] Secure cookie flags enabled
- [ ] HSTS enabled with appropriate max-age
- [ ] Content Security Policy configured (optional but recommended)

### ✅ Database Security

- [ ] Database only used for Django sessions (no user data)
- [ ] Database credentials secured
- [ ] Database access restricted to application only
- [ ] Regular database backups (if needed for sessions)

### ✅ Dependency Security

- [ ] All dependencies up to date
- [ ] No known security vulnerabilities in packages
- [ ] `pip-audit` or similar tool run regularly
- [ ] Regular dependency updates scheduled

### ✅ Error Handling

- [ ] Custom error pages for 400, 403, 404, 500
- [ ] Error messages don't leak sensitive information
- [ ] Stack traces hidden in production
- [ ] Errors logged securely without sensitive data

### ✅ Monitoring & Logging

- [ ] Application logs configured and rotating
- [ ] Failed authentication attempts logged
- [ ] Rate limit violations logged
- [ ] Error monitoring service configured (optional: Sentry, etc.)
- [ ] Log access restricted to authorized personnel

### ✅ Infrastructure Security

- [ ] Server firewall configured
- [ ] SSH key-based authentication only (no passwords)
- [ ] Regular security updates applied to OS
- [ ] Non-root user runs the application
- [ ] Unnecessary services disabled

### ✅ Testing

- [ ] Security-focused tests written and passing
- [ ] Penetration testing conducted (if applicable)
- [ ] File upload exploits tested
- [ ] CSRF protection tested
- [ ] Authentication bypass attempts tested

### ✅ Compliance

- [ ] GDPR compliance verified (EU users)
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] Data processing agreement with LLM provider
- [ ] User consent mechanisms in place

## Security Commands

### Check for vulnerabilities in dependencies
```bash
pip install pip-audit
pip-audit
```

### Generate strong Django secret key
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Check file permissions
```bash
# Unix/Linux
chmod 600 firebase-credentials.json
chmod 600 .env
```

### Scan for exposed secrets
```bash
git secrets --scan-history  # After installing git-secrets
```

## Incident Response

If security breach suspected:

1. **Immediately** rotate all API keys (Firebase, OpenAI)
2. Review application logs for suspicious activity
3. Check rate limiting logs
4. Verify no unauthorized Firebase sign-ins
5. Review server access logs
6. Notify users if data exposure suspected (though app stores nothing)

## Regular Security Tasks

- **Weekly**: Review application logs for anomalies
- **Monthly**: Update dependencies and check for vulnerabilities
- **Quarterly**: Review and update security configurations
- **Yearly**: Complete security audit and penetration test

---

**Last Updated:** January 2026
**Next Review:** [Set date 3 months from now]
