from django import VERSION
from django.conf import settings

if VERSION < (1, 8):
    def get_template_loaders():
        from django.template import loader
        return tuple(
            loader.find_template_loader(i)
            for i in settings.TEMPLATE_LOADERS
        )
else:
    def get_template_loaders():
        from django.template import engine
        return engine.Engine.get_default().template_loaders


def get_template_source(name):
    '''
    :rtype: tuple(source text, path)
    '''
    for loader in get_template_loaders():
        try:
            return loader.load_template_source(name)
        except:
            pass
    return (None, None)
