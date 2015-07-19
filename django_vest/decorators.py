# coding: utf-8
import inspect
from functools import wraps

import six

from django_vest.config import settings
from django.utils.decorators import available_attrs
from django.contrib.auth.decorators import user_passes_test

__ALL__ = ('themeble', 'only_for')


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

        if name in context and not getattr(context[name], '__themeble', False):
            raise RuntimeError(
                'Name {} already exists in this context!'.format(name))

        if ((themes and settings.CURRENT_THEME in themes) or
                (themes is None and name not in context)):
            context[name] = obj
            obj.__themeble = True

        return obj
    return wrap


def only_for(theme, redirect_to='/', raise_error=None):
    """ Decorator for restrict access to views according by list of themes.

    Params:

        * ``theme`` - string or list of themes where decorated view must be
        * ``redirect_to`` - url or name of url pattern for redirect
            if CURRENT_THEME not in themes
        * ``raise_error`` - error class for raising

    Example:

    .. code:: python

        # views.py

        from django_vest import only_for

        @only_for('black_theme')
        def my_view(request):
            ...
    """
    def check_theme(*args, **kwargs):
        if isinstance(theme, six.string_types):
            themes = (theme,)
        else:
            themes = theme

        if settings.CURRENT_THEME is None:
            return True

        result = settings.CURRENT_THEME in themes

        if not result and raise_error is not None:
            raise raise_error

        return result

    return user_passes_test(check_theme, login_url=redirect_to)
