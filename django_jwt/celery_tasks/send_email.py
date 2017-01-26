from .celery import app as celeryApp
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings
import random


@celeryApp.task(bind=True, max_retries=None)
def send_email(self, receivers, template_path, template_context, subject):
    """
    Sends an email in the background using django's email backend.
    template_path should be an absolute path to the template file.
    template_context should be a dict of bindings.
    receivers should be a list of strings
    subject should be a string
    """
    try:
        template = get_template(template_path)
        body = template.render(template_context)
        send_mail(subject, body, settings.FROM_EMAIL_ADDRESS,
                  receivers, fail_silently=False)
    except Exception as exc:
        countdown = int((random.uniform(2, 4) ** self.request.retries) * 60)
        self.retry(exc=exc, countdown=countdown, max_retries=None)
