import random

from django.http import JsonResponse
from ratelimit.userlimit import validate_user_limit

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR')

        try:
            user_limit_info = validate_user_limit(user_ip)
        except Exception as e:
            response = JsonResponse({'error':'Server error'}, status=502)
            response['Retry-After'] = random.randint(30, 60)
            return response

        if not user_limit_info['allow']:
            response = JsonResponse({'error':'limit reached try after few minutes'}, status=429)
            response['Retry-After'] = user_limit_info['Retry-After']
            return response


        response = self.get_response(request)

        return response