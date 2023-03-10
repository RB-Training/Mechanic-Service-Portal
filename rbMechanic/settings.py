"""
Django settings for rbMechanic project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')  # ^_^ ENTERED MANUALLY ^_^


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ir_r0pz8e#mcy-hf7pn4ndn4$ns4jft^d#l6dg2u0a0q=15c*h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'materializecssform',  # ^_^ ENTERED MANUALLY
    'portal'      # ^_^ ENTERED MANUALLY ^_^
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rbMechanic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],     # ^_^ ENTERED MANUALLY ^_^
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rbMechanic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES={                                         # ^_^ ENTERED MANUALLY ^_^
   'default':{                                      # ^_^ ENTERED MANUALLY ^_^
      'ENGINE':'django.db.backends.postgresql',     # ^_^ ENTERED MANUALLY ^_^

      'NAME':'ui',                            # ^_^ ENTERED MANUALLY ^_^
      'USER':'postgres',                            # ^_^ ENTERED MANUALLY ^_^
      'PASSWORD':'123$1',                            # ^_^ ENTERED MANUALLY ^_^

      'NAME':'mechanicPortalDB',                            # ^_^ ENTERED MANUALLY ^_^
      'USER':'postgres',                            # ^_^ ENTERED MANUALLY ^_^
      'PASSWORD':'1234',                            # ^_^ ENTERED MANUALLY ^_^

      'HOST':'localhost',                           # ^_^ ENTERED MANUALLY ^_^
      'PORT':'5432',                                # ^_^ ENTERED MANUALLY ^_^
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

STATICFILES_DIRS = [             # ^_^ ENTERED MANUALLY ^_^
    BASE_DIR , "static",         # ^_^ ENTERED MANUALLY ^_^
    '/var/www/static/',          # ^_^ ENTERED MANUALLY ^_^
]
