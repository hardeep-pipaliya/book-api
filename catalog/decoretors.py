from django.conf import settings
from django.http import HttpResponse, JsonResponse


def required_api_key(view_func):
    def wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get("X-API-key")
        
        if not api_key or api_key not in settings.API_KEYS:
            return  JsonResponse({
                "error" : "invalid api-key",
                "message" : "missing or invalid api-key"
             }, status = 401)
            
        return view_func(request, *args, **kwargs)
    return wrapped_view

