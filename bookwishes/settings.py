
from pathlib import Path
import os
from django.contrib.messages import constants as messages




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ri-x6=4vjrt#)7l$ke$amxgvf_#(mz=da^xy-roan&mei=16)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ip = "http://3.111.13.6/"

ALLOWED_HOSTS = ["*"]
if DEBUG:
    ip = "http://127.0.0.1:8000/"
    # ip = "http://15.206.15.234/"
else:
    ip = "https://thebookwishesclub.com/"
# Application definition

INSTALLED_APPS = [
    # 'daphne',
    # 'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #extras
    'django.contrib.sites',
    
    #Events

    'event_app',

    #custom apps
    'user_accounts',
    'club',
    'feed',
    'notification',
    'assesment', 
    'points_and_badges',
    'logs',
    'library',
    'my_forms',
    # 'app',   

    'corsheaders',

    #libraries
    'django_summernote',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'website',
    'superuser',
    'django_celery_results',
    'django_celery_beat',
    'widget_tweaks',
    

    # 'rest_auth',
    # 'rest_auth.registration',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'django_rest_passwordreset',
]

AUTH_USER_MODEL = 'user_accounts.CustomUser'

MIDDLEWARE = [
    # middleware for heroku deployment
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # middleware for cors headers
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookwishes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'superuser.context_processors.extras',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookwishes.wsgi.application'
ASGI_APPLICATION = 'bookwishes.asgi.application'
# ASGI_APPLICATION = 'core.asgi.application'
X_FRAME_OPTIONS = "SAMEORIGIN"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


if DEBUG:
    # Local Database For Testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'bookwish4',
            'USER': 'postgres',
            'PASSWORD': '1234',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }


    #  DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'bookwishes',
    #         'USER': 'postgres',
    #         'PASSWORD': '4hsi6kJIpkIb',
    #         'HOST': '/tmp/',
    #         'PORT': '5432',        
    #     }
    # }
     
    # staging database 
#    DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'bookwishes',
#             'USER': 'postgres',
#             'PASSWORD': 'LHEeUiRrtTl9',
#             'HOST': '/tmp/',
#             'PORT': '5432',        
#         }
#     } 
else:
    # AWS LIGHT SAIL DATABASES
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'bookwishes',
            'USER': 'postgres',
            'PASSWORD': '4hsi6kJIpkIb',
            'HOST': '/tmp/',
            'PORT': '5432',        
        }
    } 

    # staging
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'bookwishes',
    #         'USER': 'postgres',
    #         'PASSWORD': 'LHEeUiRrtTl9',
    #         'HOST': '/tmp/',
    #         'PORT': '5432',        
    #     }
    # } 




# ElephantSQL Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'fzsgwusg',
#         'USER': 'fzsgwusg',
#         'PASSWORD': 'NARH5M7tXIf2PjQHezeDjpb1-riu0hvz',
#         'HOST': 'tiny.db.elephantsql.com',
#     }
# } 



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'fzsgwusg',
#         'USER': 'fzsgwusg',
#         'PASSWORD': 'NARH5M7tXIf2PjQHezeDjpb1-riu0hvz',
#         'HOST': 'tiny.db.elephantsql.com',
#     }
# } 



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'bookwishes2',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# } 

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True

USE_I18N = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# STATICFILES_DIRS = [
#     BASE_DIR / "superuser/static",
#     BASE_DIR / "static",
# ]
# for django summernote media files
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



STATIC_ROOT = os.path.join(BASE_DIR, 'static')
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kathmandu'


# CELERY BEAT 

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
     'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]   
}

SITE_ID = 1

# for email

if DEBUG:
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
# EMAIL_HOST_USER = 'bloggingworkshop046@gmail.com'
# EMAIL_HOST_PASSWORD = 'hngn nrxh asps pitt'
EMAIL_HOST_USER = 'thebookwishesclub@gmail.com'
EMAIL_HOST_PASSWORD = 'dpma rohm xjhk zahn'





CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# CORS_ALLOWED_ORIGINS = [
# "https://thebookwishesclub.com",
# ]


# CORS_ORIGINS_ALLOW_ALL = True
# CORS_ALLOW_ALL_ORIGINS = True