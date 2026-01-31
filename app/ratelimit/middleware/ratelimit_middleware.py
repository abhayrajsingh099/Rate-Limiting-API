from django.http import JsonResponse
from ratelimit.userlimit import validate_user_limit

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR')

        user_limit_info = validate_user_limit(user_ip)

        if not user_limit_info:
            response = JsonResponse({'error':'limit reached try after few mintues'}, status=429)
            response['Retry-After'] = 60
            return response


        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response