_F = '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {},
    'formatters': {
        'verbose': {'format': _F, },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG', 'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR', 'handlers': ['console'], 'propagate': False,
        },
    },
}
