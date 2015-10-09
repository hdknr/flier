__all__ = ('__version__', '__build__', 'get_version', 'conf', )
__version__ = (0, 0, 1)
__build__ = ''


def get_version():
    return '.'.join(map(lambda v: str(v), __version__))

default_app_config = 'flier.smtp.apps.AppConfig'
