from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class CSRFFailureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            logger.warning(f"CSRF failure occurred for request: {request.path}")
            return redirect(reverse('core:login_view'))