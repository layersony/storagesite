import os
import django_heroku
import dj_database_url
from decouple import config, Csv

from django.contrib.messages import constants as messages


MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
MODE = config('MODE', default='dev')

AUTH_USER_MODEL = 'mainapp.User'

INSTALLED_APPS = [
    'mpesa_api.apps.MpesaApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'customer',
    'employee',
    'bootstrap4',
    'rest_framework',
    'rest_framework.authtoken',
    # 'django_daraja',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'storagesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'storagesite.wsgi.application'

if config('MODE')=='dev':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS =['.localhost','.herokuapp.com','127.0.0.1', '29f0b3481c82.ngrok.io']


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())

LOGIN_REDIRECT_URL ='/'
LOGOUT_REDIRECT_URL ='/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

EMAIL_USE_TLS = True
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER=config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')



# # The Mpesa environment to use
# # Possible values: sandbox, production

# MPESA_ENVIRONMENT = 'sandbox'

# # Credentials for the daraja app

# MPESA_CONSUMER_KEY = 'n7jvs1RC3BDZ1OzPoF7HkAjLDyHMmRdG'
# MPESA_CONSUMER_SECRET = 'XbXDA8TNflXWuZAc'

# #Shortcode to use for transactions. For sandbox  use the Shortcode 1 provided on test credentials page

# MPESA_SHORTCODE = '174379'

# # Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
# # This is only used on sandbox, do not set this variable in production
# # For sandbox use the Lipa na MPESA Online Shorcode provided on test credentials page

# MPESA_EXPRESS_SHORTCODE = '174379'

# # Type of shortcode
# # Possible values:
# # - paybill (For Paybill)
# # - till_number (For Buy Goods Till Number)

# MPESA_SHORTCODE_TYPE = 'paybill'

# # Lipa na MPESA Online passkey
# # Sandbox passkey is available on test credentials page
# # Production passkey is sent via email once you go live

# MPESA_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919!'

# # Username for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

# MPESA_INITIATOR_USERNAME = 'testapi'

# # Plaintext password for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

# MPESA_INITIATOR_SECURITY_CREDENTIAL = 'Safaricom992!'