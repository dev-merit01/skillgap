"""
Views for SkillGap application.
Handles landing page, app page, text extraction, and CV analysis endpoints.
"""
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .services.firebase_auth import FirebaseAuthService
from .services.cv_parser import CVParserService
from .services.document_extractor import (
    DocumentTextExtractor,
    DocumentExtractionError,
)
from .services.llm_client import LLMClientService

logger = logging.getLogger(__name__)




def _authenticate_request(request):
    """
    Helper to authenticate Firebase token from request.
    Returns user_info dict or raises ValueError.
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise ValueError('Missing or invalid authorization header')
    
    id_token = auth_header.split('Bearer ')[1].strip()
    return FirebaseAuthService.verify_token(id_token)


@require_http_methods(["GET"])
def landing(request):
    """
    Marketing landing page view.
    """
    return render(request, 'analyzer/landing.html')


@require_http_methods(["GET"])
def register(request):
    """
    User registration page view.
    """
    return render(request, 'analyzer/register.html')


@require_http_methods(["GET"])
def login_view(request):
    """
    User login page view.
    """
    return render(request, 'analyzer/login.html')


@require_http_methods(["GET"])
def forgot_password(request):
    """
    Forgot password page view.
    """
    return render(request, 'analyzer/forgot_password.html')


@require_http_methods(["GET"])
def app(request):
    """
    Application page view with job description input and CV upload form.
    """
    context = {
        'max_file_size_mb': settings.MAX_UPLOAD_SIZE / (1024 * 1024),
        'allowed_extensions': ', '.join(settings.ALLOWED_FILE_EXTENSIONS),
        'allowed_extensions_list': settings.ALLOWED_FILE_EXTENSIONS,
        'image_ocr_enabled': bool(getattr(settings, 'OPENAI_API_KEY', None)),
        'max_job_length': settings.MAX_JOB_DESCRIPTION_LENGTH,
    }
    return render(request, 'analyzer/home.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def extract_jd_text(request):
    """
    Extract text from uploaded job description file.
    Returns extracted text for user review before analysis.
    
    Expected request:
        - Headers: Authorization: Bearer <firebase_id_token>
        - Files: jd_file (PDF, DOCX, or image)
    
    Returns:
        JSON with extracted_text for user to review/edit
    """
    try:
        # Authenticate
        try:
            user_info = _authenticate_request(request)
            logger.info(f"Extract JD request from: {user_info['email']}")
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=401)
        
        # Validate file present
        if 'jd_file' not in request.FILES:
            return JsonResponse({
                'error': 'No file uploaded. Please select a file.'
            }, status=400)
        
        jd_file = request.FILES['jd_file']
        
        # Extract text using new service
        try:
            extracted_text = DocumentTextExtractor.extract(jd_file, jd_file.name)
        except DocumentExtractionError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        logger.info(f"Extracted {len(extracted_text)} chars from JD for {user_info['email']}")
        
        return JsonResponse({
            'success': True,
            'extracted_text': extracted_text,
            'char_count': len(extracted_text),
            'filename': jd_file.name,
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in extract_jd_text: {e}", exc_info=True)
        return JsonResponse({
            'error': 'An unexpected error occurred while processing the file.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def analyze(request):
    """
    Main analysis endpoint. Requires Firebase authentication.
    Processes CV and job description TEXT, returns LLM analysis.
    
    Expected request:
        - Headers: Authorization: Bearer <firebase_id_token>
        - POST data: job_description (text - already extracted or pasted)
        - Files: cv_file (PDF or DOCX)
    
    Returns:
        JSON response with match analysis or error message
    """
    try:
        # Step 1: Authenticate
        try:
            user_info = _authenticate_request(request)
            logger.info(f"Analyze request from: {user_info['email']}")
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=401)
        
        user_email = user_info['email']

        # Step 2: Get job description TEXT (must be provided directly)
        job_description = request.POST.get('job_description', '').strip()
        
        if not job_description:
            return JsonResponse({
                'error': 'Job description is required. Please paste or extract text first.'
            }, status=400)
        
        if len(job_description) < 100:
            return JsonResponse({
                'error': 'Job description is too short. Please provide more details.'
            }, status=400)
        
        if len(job_description) > settings.MAX_JOB_DESCRIPTION_LENGTH:
            return JsonResponse({
                'error': f'Job description exceeds maximum length of {settings.MAX_JOB_DESCRIPTION_LENGTH} characters'
            }, status=400)
        
        # Step 3: Check for CV file
        if 'cv_file' not in request.FILES:
            return JsonResponse({
                'error': 'CV file is required'
            }, status=400)
        
        cv_file = request.FILES['cv_file']
        
        # Step 4: Parse CV (in memory)
        try:
            cv_text = CVParserService.parse_cv(cv_file, cv_file.name)
            logger.info(f"Parsed CV for: {user_info['email']} ({len(cv_text)} chars)")
            
            # Validate CV text is substantial enough
            if len(cv_text.strip()) < 50:
                return JsonResponse({
                    'error': 'CV text is too short or empty. Please ensure the CV file contains readable text. If you uploaded an image, check that the text extraction worked properly.'
                }, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        # Step 5: Perform LLM analysis
        try:
            analysis_result = LLMClientService.analyze(cv_text, job_description)
            logger.info(f"Analysis complete for: {user_info['email']}")
        except ValueError as e:
            return JsonResponse({
                'error': f'Analysis failed: {str(e)}'
            }, status=500)
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}")
            return JsonResponse({
                'error': 'An unexpected error occurred during analysis'
            }, status=500)
        
        # Return results
        return JsonResponse({
            'success': True,
            'user': {
                'email': user_info['email'],
                'name': user_info['name']
            },
            'analysis': analysis_result,
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze view: {e}", exc_info=True)
        return JsonResponse({
            'error': 'An unexpected error occurred'
        }, status=500)


@require_http_methods(["GET"])
def debug_info(request):
    """
    Debug endpoint to check Firebase and system configuration.
    Only available in DEBUG mode.
    """
    if not settings.DEBUG:
        return JsonResponse({'error': 'Not available'}, status=403)
    
    debug_info = {
        'debug_mode': settings.DEBUG,
        'firebase_auth_disabled': getattr(settings, 'FIREBASE_AUTH_DISABLED', False),
        'firebase_credentials_path': bool(settings.FIREBASE_CREDENTIALS_PATH),
        'firebase_project_id': bool(settings.FIREBASE_PROJECT_ID),
        'firebase_service_account_json': bool(settings.FIREBASE_SERVICE_ACCOUNT_JSON),
        'openai_api_key': bool(settings.OPENAI_API_KEY),
        'allowed_hosts': settings.ALLOWED_HOSTS,
    }
    
    return JsonResponse(debug_info)


@csrf_exempt
@require_http_methods(["POST"])
def test_openai_extraction(request):
    """
    Test OpenAI Vision API extraction on uploaded image.
    Returns extraction details and raw text for debugging.
    
    Expected:
        - Files: image_file (PNG, JPG, JPEG)
    
    Returns:
        JSON with extraction status, text length, and sample
    """
    try:
        # Check API key
        if not settings.OPENAI_API_KEY:
            return JsonResponse({
                'error': 'OpenAI API key not configured',
                'status': 'FAILED'
            }, status=400)
        
        # Validate file
        if 'image_file' not in request.FILES:
            return JsonResponse({
                'error': 'No image file uploaded',
                'status': 'FAILED'
            }, status=400)
        
        image_file = request.FILES['image_file']
        filename = image_file.name
        
        # Read file content
        file_content = image_file.read()
        
        # Try OpenAI extraction
        try:
            from analyzer.services.document_extractor import ImageOCRExtractor
            
            logger.info(f"Testing OpenAI extraction for: {filename}")
            extracted_text = ImageOCRExtractor.extract(file_content, document_type="jd")
            
            return JsonResponse({
                'status': 'SUCCESS',
                'filename': filename,
                'extracted_length': len(extracted_text),
                'sample': extracted_text[:500],
                'full_text': extracted_text,
                'message': f'Successfully extracted {len(extracted_text)} characters using OpenAI Vision API'
            })
            
        except Exception as e:
            logger.error(f"OpenAI extraction test failed: {e}", exc_info=True)
            return JsonResponse({
                'status': 'FAILED',
                'error': str(e),
                'filename': filename,
                'message': 'OpenAI extraction failed - check API key and image quality'
            }, status=500)
    
    except Exception as e:
        logger.error(f"Test endpoint error: {e}", exc_info=True)
        return JsonResponse({
            'status': 'FAILED',
            'error': str(e)
        }, status=500)
