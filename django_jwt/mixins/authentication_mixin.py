from django.conf import settings
from time import time
from jose import jwt
import hmac
import base64
import hashlib


class AuthenticationMixin(object):
    """
    Profile Authentication related logic.
    Author: Ahmed H. Ismail
    """

    def generate_token(self, expiration):
        """
        Generates an authentication token for this profile.
        Expiration in seconds.
        Author: Ahmed H. Ismail
        """
        claims = {
            'profile_pk': self.pk,
            'pk': hmac.new(settings.HASHING_SECRET.encode('utf-8'),
                self.user.password.encode('utf-8'), hashlib.sha512).hexdigest().lower(),
            'exp': int(time()) + expiration,
            'sub_type': 'authentication'
        }
        return base64.urlsafe_b64encode(jwt.encode(
            claims, settings.TOKEN_JWT_SECRET, settings.TOKEN_JWT_ALGO).encode('utf-8')).decode('utf-8')

    @classmethod
    def from_token(cls, b64_token):
        """
        Retrieves profile by token.
        Raises jose.jwt.ExpiredSignatureError if token has expired
        Raises jose.jwt.JWTError if invalid JWT
        Author: Ahmed H. Ismail
        """
       
        token  = base64.urlsafe_b64decode(b64_token)
        decoded = jwt.decode(token, settings.TOKEN_JWT_SECRET, algorithms=[settings.TOKEN_JWT_ALGO])
        if decoded['sub_type'] != 'authentication':
            raise jwt.JWTError('Unknown token type')
        profile = cls.objects.filter(pk=decoded['profile_pk'])
        if profile.count() == 0:
            raise jwt.JWTError('Invalid token')
        profile = profile[0]
        phash = hmac.new(settings.HASHING_SECRET.encode('utf-8'),
            profile.user.password.encode('utf-8'), hashlib.sha512).hexdigest().lower()
        if hmac.compare_digest(phash, decoded['pk']):
            return profile
        else:
            raise jwt.ExpiredSignatureError('Expired token')
