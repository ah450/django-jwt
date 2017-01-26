from django_jwt.celery_tasks import send_email
from django.conf import settings
from jose import jwt
from time import time
import base64
import hmac
import hashlib
import os

class ActivationMixin(object):
    """
    Handles account activation logic
    """

    def gen_activation_token(self):
        """
        Generates an account activation token.
        Author: Ahmed H. Ismail
        """
        
        claims = {
            'profile_pk': self.pk,
            'pk': hmac.new(settings.HASHING_SECRET.encode('utf-8'),
                self.user.email.encode('utf-8'), hashlib.sha512).hexdigest().lower(),
            'sub_type': 'activation'
        }
        return base64.urlsafe_b64encode(jwt.encode(claims, settings.ACTIVATION_JWT_SECRET,
            settings.ACTIVATION_JWT_ALGO).encode('utf-8')).decode('utf-8')

    @classmethod
    def activate_profile(cls, b64_token):
        """
        Returns profile if verified.
        jose.jwt.JWTError if invalid JWT
        Author: Ahmed H. Ismail
        """
        token = base64.urlsafe_b64decode(b64_token)
        decoded = jwt.decode(token, settings.ACTIVATION_JWT_SECRET, algorithms=[settings.ACTIVATION_JWT_ALGO])
        if decoded['sub_type'] != 'activation':
            raise jwt.JWTError('Invalid Token')
        profile = cls.objects.filter(pk=decoded['profile_pk'])
        if profile.count() == 0:
            raise jwt.JWTError('Invalid token')
        profile = profile[0]
        if not hmac.compare_digest(decoded['pk'], hmac.new(settings.HASHING_SECRET.encode('utf-8'),
            profile.user.email.encode('utf-8'), hashlib.sha512).hexdigest().lower()):
            raise jwt.JWTError('Invalid Token')
        profile.active = True
        profile.user.is_active = True
        profile.user.save()
        profile.save()
        return profile

    def send_activation_mail(self):
        token = self.gen_activation_token()
        template = settings.email_templates_dir
        template = os.path.join(template, 'activate_account.txt')
        context = {
            'name': "{0} {1}".format(self.user.first_name, self.user.last_name),
            'email': self.user.email,
            'link': "https://{0}/#/activate?token={1}".format(settings.BASE_HOST, token)
        }
        send_email.delay([self.user.email], template,
                         context, '[{0}] Activate Account'.format(settings.email_subject))