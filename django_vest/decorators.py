# coding: utf-8
from django_vest import config

__ALL__ = ('themeble',)


def themeble(name, themes=None):
    """ Decorator for registering objects (i.e. functions, classes) for
    different themes.

    Params:

        * name - type of string. New global name for object
        * themes - for this themes ``obj`` will be have alias with given name


    Example:

    .. code:: python

        @themeble(name='Form', themes=('dark_theme',))
        class DarkThemeForm(object):
            ''' Some kind of logic for dark_theme
            '''
            name = 'DarkThemeForm'


        @themeble(name='Form')
        class DefaultForm(object):
            ''' Default logic for all themes
            '''
            name = 'Default form'


    Now if settings.CURRENT_THEME == 'dark_theme':

    .. code:: python

        from django_vest.decorators import Form
        Form.name # we got DarkThemeForm

    """
    def wrap(obj):
        if themes and config.CURRENT_THEME in themes:
            globals()[name] = obj

        elif themes is None and name not in globals():
            globals()[name] = obj

        return obj
    return wrap
