import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(name):
    """ Gets the specified environment variable.

    :param name: The name of the variable.
    :type name: str
    :returns: The value of the specified variable.
    :raises: **ImproperlyConfigured** when the specified variable does not exist.

    """

    try:
        return os.environ[name]
    except KeyError:
        error_msg = "The %s environment variable is not set!" % name
        raise ImproperlyConfigured(error_msg)


# ================================================================================================ #
#                                         General Management                                       #
# ================================================================================================ #

ADMINS = (
    ('Alex Kavanaugh', 'kavanaugh.development@outlook.com'),
    ('Kyle Reis', 'fedorareis@gmail.com'),
)

MANAGERS = ADMINS

# ================================================================================================ #
#                                         General Settings                                         #
# ================================================================================================ #

# Local time zone for this installation. Choices can be found here:
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation.
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

DATE_FORMAT = 'l, F d, Y'

TIME_FORMAT = 'h:i a'

DATETIME_FORMAT = 'l, F d, Y h:i a'

DEFAULT_CHARSET = 'utf-8'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# ================================================================================================ #
#                                          File Names                                              #
# ================================================================================================ #

PHILO_ADMIN_FILENAME = "philo_admin"
PHILO_RESIDENT_FILENAME = "usernames_emails"
NOTIFII_RESIDENT_FILENAME = "50154"

# ================================================================================================ #
#                                          Database Configuration                                  #
# ================================================================================================ #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'dw': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'dwprddb.db.calpoly.edu:1521/dwprddb',
        'USER': get_env_variable('UPLOADER_DB_DW_USERNAME'),
        'PASSWORD': get_env_variable('UPLOADER_DB_DW_PASSWORD'),
    },
}

DATABASE_ROUTERS = (
    'dwconnector.routers.DWRouter',
)

# ================================================================================================ #
#                                            SFTP Configuration                                    #
# ================================================================================================ #

SFTP = {
    'philo': {
        'USER': 'calpoly',
        'PASSWORD': get_env_variable('PHILO_SFTP_PASSWORD'),
        'HOST': 'calpoly.philo.com',
        'PORT': '22',
    },
    'notifii': {
        'USER': 'P2L9dC7ww5',
        'PASSWORD': get_env_variable('NOTIFII_SFTP_PASSWORD'),
        'HOST': 'notifii.exavault.com',
        'PORT': '22',
    },
    'advocate': {
        'USER': 'calpolydrop',
        'PASSWORD': None,  # Using key exchange
        'HOST': 'calpoly-advocate.symplicity.com',
        'PORT': '22',
    }
}

# ================================================================================================ #
#                                        LDAP Groups Configuration                                 #
# ================================================================================================ #

LDAP_GROUPS_SERVER_URI = 'ldap://ad.calpoly.edu'
LDAP_GROUPS_BASE_DN = 'DC=ad,DC=calpoly,DC=edu'

LDAP_GROUPS_BIND_DN = get_env_variable('UPLOADER_LDAP_USER_DN')
LDAP_GROUPS_BIND_PASSWORD = get_env_variable('UPLOADER_LDAP_PASSWORD')

LDAP_GROUPS_USER_LOOKUP_ATTRIBUTE = 'sAMAccountName'
LDAP_GROUPS_ATTRIBUTE_LIST = [LDAP_GROUPS_USER_LOOKUP_ATTRIBUTE, 'userPrincipalName']

ADMIN_AD_GROUP = "CN=UH-philo,OU=Websites,OU=UH,OU=Manual,OU=Groups,DC=ad,DC=calpoly,DC=edu"

# ================================================================================================ #
#                                      Session/Security Configuration                              #
# ================================================================================================ #

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('UPLOADER_SECRET_KEY')

# ================================================================================================ #
#                                  File/Application Handling Configuration                         #
# ================================================================================================ #

PROJECT_DIR = Path(__file__).parents[2]

# The directory that will hold temporary export files.
MEDIA_ROOT = str(PROJECT_DIR.joinpath("media").resolve())

# The directory that holds configuration files, such as SFTP keys
CONFIG_ROOT = str(PROJECT_DIR.joinpath("conf").resolve())

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'raven.contrib.django.raven_compat',
    'uploader.apps.core',
    'dwconnector',
)

# ================================================================================================ #
#                                         Logging Configuration                                    #
# ================================================================================================ #

RAVEN_CONFIG = {
    'dsn': get_env_variable('SENTRY_DSN'),
    'tags': {'uploader': 'service_uploader'},
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'service_uploader.apps.core.utils': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
