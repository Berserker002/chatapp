from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone

class TokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.auth, 'created'):
            token = request.auth
            current_time = timezone.now()
            token_expiration_time = token.created + timezone.timedelta(hours=1)

            if current_time >= token_expiration_time:
                request.user.is_online = False
                request.user.save()

        response = self.get_response(request)
        return response
