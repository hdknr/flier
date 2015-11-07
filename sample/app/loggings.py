_F = '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING', 'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {'format': _F, },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG', 'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR', 'handlers': ['console'], 'propagate': False,
        },
        'raven': {
            'level': 'DEBUG', 'handlers': ['console'], 'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG', 'handlers': ['console'], 'propagate': False,
        },
    },
}
