import os

from celery import task
from django.conf import settings

from adapter.email import EmailAdapter
from cache.weathercache import WeatherCache


@task(name="email_weather_report")
def email_weather_report(email_list):
    weatherCache = WeatherCache()
    data = weatherCache.get_configuration()
    file_path = os.path.join(settings.MEDIA_ROOT, "weather-report.xlsx")
    for email in email_list:
        emailAdapter = EmailAdapter(email)
        emailAdapter.send_email(has_attachments=True, file_path=file_path)
