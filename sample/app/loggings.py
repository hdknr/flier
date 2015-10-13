import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_F = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': _F, 'datefmt': "%d/%b/%Y %H:%M:%S"},
        'simple': {'format': '%(levelname)s %(message)s'},
    },
    'handlers': {
        'file': {
            'level': 'DEBUG', 'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'app.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {'handlers': ['file'], 'propagate': True, 'level': 'DEBUG'},
        'flier': {'handlers': ['file'], 'level': 'DEBUG', },
    }
}
