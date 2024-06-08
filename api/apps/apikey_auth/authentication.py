from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import ApiKey


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')

        if not api_key:
            raise AuthenticationFailed('Missing API key')

        try:
            user = ApiKey.objects.get(key=api_key).user
        except ApiKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')

        return (user, None)
