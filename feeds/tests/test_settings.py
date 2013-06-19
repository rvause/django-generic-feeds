INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'feeds',
    'feeds.tests'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

SECRET_KEY = 'none'
