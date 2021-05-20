from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

FLAVOUR = "development"
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'account.AppUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

}

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_ROUTES = {
    'account.api.tasks.email_weather_report': {'queue': 'default'},
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
        },
    }
}

WEATHER_API = {
    "URL": "http://api.openweathermap.org/data/2.5/find",
    "PARAMETER_NAMES": {
        "latitude": "lat",
        "longitude": "lon",
        "count": "cnt",
        "secret_key": "appid"
    },
    "PARAMETER_VALUES": {
        "latitude": 55.5,
        "longitude": 37.5,
        "count": 30,
        "secret_key": ""
    }

}

# EMAIL CREDENTIALS
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jinay.aft@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
