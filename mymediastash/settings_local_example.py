DEBUG = True
SECRET_KEY = 'django-insecure-br(wo%f017wdrqvl6o#$@cja+6z-6b8h5*v44t++)%z-qpb0il'
ALLOWED_HOSTS = ['127.0.0.1']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mymediastash',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': 5432
    }
}

# Base installed apps
ALWAYS_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mymediastash',
]

# Installed modules
INSTALLED_APPS = ALWAYS_INSTALLED_APPS + [
    'book',
]

# Localization
LANGUAGE_CODE = 'cs'
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and media files
STATIC_ROOT = 'static/'
STATIC_URL = 'static/'
MEDIA_ROOT = 'media/'
MEDIA_URL = 'media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
