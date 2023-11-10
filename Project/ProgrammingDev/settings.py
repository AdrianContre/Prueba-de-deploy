"""
Django settings for ProgrammingDev project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g1o--qykz&0k*j_#-a%xh-!+9o%ms0$hm^7mg@oln@(7#wfu2!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'ProgrammingDev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProgrammingDev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',
   #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway', 
        'USER': 'postgres',
        'PASSWORD': 'bbbCF4edGBg*c1gCaCa1g33eCG5Fbd5c',
        'HOST': 'monorail.proxy.rlwy.net', 
        'PORT': '24537',
    }
}

AUTH_USER_MODEL = 'app.User'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIRS = os.path.join(BASE_DIR,'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build','static')


#AWS
AWS_ACCESS_KEY_ID = 'ASIASM6MPIBCBG7VNYXW'
AWS_SECRET_ACCESS_KEY = 'JKxHGJTHOKPKBO0GLIi/xk1CUlpukbJDr/RcLrhc'
AWS_STORAGE_BUCKET_NAME = 'storageasw'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_SESSION_TOKEN = 'FwoGZXIvYXdzECEaDLQ20ap4XDrzTtcMkSLRAd6M2OgPVtFBC964QTRV0ttuq5ykcRWa1v26Ev32adF9Ahpus+Gqgj/iJUgmJIiP1azhmrTcNHrClOtaCP+VzkSd6znsmjaYZuOlWUP8sujI3sx+buo2yinzXG7LAcBEa5OXKYU1FXiRI0eNWL/Z3DQzqS78neJV4MuEypjmrn4rp7S05WcS2KUqoOjYcWhigXBOCDt6BMzTia/raBQ/3qI2WSprq1k+zpIBl9pdbAH7Qx9zSfsZKmf8yPDuYsWXnlgZ7LZHuDapIIoK/WkSdkcUKOmwlKoGMi2vDPruaao9Hv2c4EB5v3oYe5JJbHayOQBDEZUjmTxIvnBZRVXP0gM5tLWpKQY='

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Primary Key default field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_AVATAR = 'https://s3.amazonaws.com/storageasw/avatars/corazon.png'

#social app settings
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'index'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '809663829226-ujtcokq05eb456mj1ogo9ufo5si6p0tc.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
