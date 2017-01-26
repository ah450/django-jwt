import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue


# set the default Django settings module for the 'celery' program.
app = Celery("{0}_jwt_celery".format(settings.jwt_realm))

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.conf['CELERY_DEFAULT_QUEUE'] = "{0}-jwt-celery-queue".format(settings.jwt_realm)
CELERY_QUEUES = (
    Queue("{0}-jwt-celery-queue".format(settings.jwt_realm), Exchange("{0}-jwt".format(settings.jwt_realm)), routing_key="{0}-jwt".format(settings.jwt_realm)),
)
app.conf['CELERY_QUEUES'] = CELERY_QUEUES
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
