from django_jwt.celery_tasks import send_email
from django.conf import settings
from jose import jwt
from time import time
import base64
import hmac
import hashlib
import os


class PasswordResetMixin(object):
    """
    Handles password reset functionality
    Author: Ahmed H. Ismail
    """
    def gen_reset_pass_token(self, expiration):
        """
        Generates a token for password reset.
        expiration in seconds.
        Author: Ahmed H. Ismail
        """
        claims = {
            'profile_pk': self.pk,
            'pk': hmac.new(settings.HASHING_SECRET.encode('utf-8'),
                self.user.email.encode('utf-8'), hashlib.sha512).hexdigest().lower(),
            'exp': int(time()) + expiration,
            'sub_type': 'reset'
        }
        return base64.urlsafe_b64encode(jwt.encode(
            claims, settings.RESET_JWT_SECRET, settings.RESET_JWT_ALGO).encode('utf-8')).decode('utf-8')

    @classmethod
    def reset_pass(cls, b64_token, new_password):
        """
        Resets password and returns Profile instance.
        Raises jose.jwt.ExpiredSignatureError if expired token
        Raises jose.jwt.JWTError if invalid token.
        Author: Ahmed H. Ismail
        """
        token = base64.urlsafe_b64decode(b64_token)
        decoded = jwt.decode(token, settings.RESET_JWT_SECRET, algorithms=[settings.RESET_JWT_ALGO])
        if decoded['sub_type'] != 'reset':
            raise jwt.JWTError('Unknown token type')
        profile = cls.objects.filter(pk=decoded['profile_pk'])
        if profile.count() == 0:
            raise jwt.JWTError('Invalid token')
        profile = profile[0]
        email_hash = hmac.new(settings.HASHING_SECRET.encode('utf-8'),
            profile.user.email.encode('utf-8'), hashlib.sha512).hexdigest().lower()
        if not hmac.compare_digest(decoded['pk'], email_hash):
            raise jwt.ExpiredSignatureError('Expired token')
        profile.user.set_password(new_password)
        profile.user.save()
        return profile

    def send_reset_mail(self):
        token = self.gen_reset_pass_token(expiration=settings.PASS_RESET_EXPIRATION)
        context = {
            'name': "{0} {1}".format(self.user.first_name, self.user.last_name),
            'email': self.user.email,
            'link': "https://{0}/#/reset_pass?token={1}".format(settings.BASE_HOST, token)
        }
        template = settings.email_templates_dir
        template = os.path.join(template, 'reset_pass.txt')
        send_email.delay([self.user.email], template,
                         context, '[{0}] Reset Password'.format(settings.email_subject))


