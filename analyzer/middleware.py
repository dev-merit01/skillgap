"""
Rate Limiting Middleware
Implements IP-based rate limiting to prevent abuse.
"""
import time
import logging
from collections import defaultdict
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    Middleware to implement rate limiting based on IP address or Firebase UID.
    Tracks request counts per identifier within a time window.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Store: {identifier: [(timestamp1, timestamp2, ...)]}
        self.request_history = defaultdict(list)
    
    def __call__(self, request):
        # Only apply rate limiting to the analyze endpoint
        if request.path == '/analyze/' and request.method == 'POST':
            # Get identifier (IP address or Firebase UID from session)
            identifier = self._get_identifier(request)
            
            # Check rate limit
            if not self._check_rate_limit(identifier):
                logger.warning(f"Rate limit exceeded for identifier: {identifier}")
                return JsonResponse({
                    'error': 'Rate limit exceeded. Please try again later.',
                    'retry_after': settings.RATE_LIMIT_WINDOW
                }, status=429)
            
            # Record this request
            self._record_request(identifier)
        
        response = self.get_response(request)
        return response
    
    def _get_identifier(self, request) -> str:
        """
        Get unique identifier for rate limiting.
        Uses Firebase UID if available, otherwise falls back to IP address.
        """
        # Try to get Firebase UID from request if available
        if hasattr(request, 'firebase_user'):
            return f"uid:{request.firebase_user['uid']}"
        
        # Fall back to IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        return f"ip:{ip}"
    
    def _check_rate_limit(self, identifier: str) -> bool:
        """
        Check if identifier is within rate limit.
        
        Args:
            identifier: Unique identifier (IP or UID)
            
        Returns:
            True if within limit, False if exceeded
        """
        current_time = time.time()
        window_start = current_time - settings.RATE_LIMIT_WINDOW
        
        # Get request history for this identifier
        request_times = self.request_history[identifier]
        
        # Remove old requests outside the time window
        self.request_history[identifier] = [
            t for t in request_times if t > window_start
        ]
        
        # Check if under the limit
        return len(self.request_history[identifier]) < settings.RATE_LIMIT_REQUESTS
    
    def _record_request(self, identifier: str) -> None:
        """
        Record a new request for the identifier.
        
        Args:
            identifier: Unique identifier (IP or UID)
        """
        self.request_history[identifier].append(time.time())
        
        # Cleanup: Remove identifiers with no recent requests
        # This prevents memory buildup over time
        current_time = time.time()
        window_start = current_time - settings.RATE_LIMIT_WINDOW
        
        identifiers_to_remove = []
        for ident, times in self.request_history.items():
            if not times or max(times) < window_start:
                identifiers_to_remove.append(ident)
        
        for ident in identifiers_to_remove:
            del self.request_history[ident]
