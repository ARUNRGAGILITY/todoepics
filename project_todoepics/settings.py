import os
from pathlib import Path
from datetime import datetime
current_year = datetime.now().year
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Step1: Clear the top level and other comments as you add steps

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Step2: Change the secret key or from environment
SECRET_KEY = 'django-dwerqwer334324-4eid=96qh*4doh3m5$=6i8y@5v2nj&%n(wsc%1%o776p7kzhap'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# Step5: add the standard apps / installations
# Step6: add the custom apps written
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Step5: add the apps
    # Installed general django libs
    'app_web.templatetags',
    'mptt',
    'crispy_forms',
    'crispy_bootstrap5',
    'markdownx',
    'markdown',    
    # Step6: written apps
    'app_web',
    'app_loginsystem',
    'app_todoepics',
    # onbranch/MVP_BASE
    'app_baseline',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_todoepics.urls'

# Step3: add th DIRS line
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_web.context_processors.settings_context_processor.get_site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_todoepics.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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



# Step2: add these
# Customized / SOP


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
TIME_ZONE = 'Asia/Kolkata'
LOGIN_URL = '/login'

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Step3: added the context processors in the app_web/context_processors/settings_context_processors.py


### Logging
# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',  # Set level based on DEBUG
    },
}
### End logging

## CUSTOMIZATION
BUILD_VERSION = 'vR1.0.10d4a'
BUILD_DESCRIPTION = 'fixing regn'
## TEMPLATE DISPLAY
SITE_TITLE = "AgileTIA"
CODING_AI = "codingagi1"
SITE_NAME = f"{SITE_TITLE}"
CONTACT_EMAIL = "contact@a{SITE_TITLE}.com"
## copyright information
PRIVACY_INFO = "No Privacy Information collected and utilized."
COPYRIGHT_INFO = f"© {current_year}. {PRIVACY_INFO} All rights reserved."

SITE_CAPTION = f"{SITE_TITLE} helps organizations and startups to transform and launch a continuous improvement and sustainable journey."

SITE_DESC = f"""
{SITE_TITLE} helps to transform small, medium and large organizations and enterprizes in a sustainable way.
"""
