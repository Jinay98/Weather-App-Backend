import os

from celery import Celery

flavour = os.environ.get('FLAVOUR', 'development')
if flavour == "development":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_app.settings.development')
elif flavour == "staging":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_app.settings.staging')
elif flavour == "production":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_app.settings.production')

celery_app = Celery('weather_app')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(['account.api'])

