# coding: utf-8
import inspect

from django_vest.config import settings

__ALL__ = ('themeble',)


def themeble(name, themes=None, global_context=None):
    """ Decorator for registering objects (i.e. functions, classes) for
    different themes.

    Params:

        * name - type of string. New global name for object
        * themes - for this themes ``obj`` will be have alias with given name
        * global_context - current decorator's global context


    Example:

    .. code:: python

        # my_app.forms.py

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

        # my_app.views.py

        from my_app.forms import Form
        assert Form.name == 'DarkThemeForm'

    """
    def wrap(obj):
        context = global_context or inspect.stack()[1][0].f_globals

        if themes and settings.CURRENT_THEME in themes:
            context[name] = obj

        elif themes is None and name not in context:
            context[name] = obj

        return obj
    return wrap
