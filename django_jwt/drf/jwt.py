from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Header/query param JWT Authentication.
    Author: Ahmed H. Ismail
    """

    def get_from_header(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token is not None:
            token = token.replace('Bearer ', '')
        return token

    def get_from_params(self, request):
        return request.GET.get('token', None)

    def authenticate(self, request):
        token = self.get_from_header(request) or self.get_from_params(request)
        if token is None:
            return None
        profile = settings.profile_klass.from_token(token)
        if not profile.active:
            raise exceptions.AuthenticationFailed('Inactive Account')
        return (profile.user, token)

    def authenticate_header(self, request):
        return 'Bearer realm={0}'.settings.jwt_realm
