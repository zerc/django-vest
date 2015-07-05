# coding: utf-8
from django.test import override_settings

from django_vest.test import TestCase
from django_vest.decorators import themeble

code_template = """
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
"""

invalid_code = """
class Form(object):
    ''' Existing form
    '''

@themeble(name='Form', themes=('dark_theme',))
class Form(object):
    ''' Some kind of logic for dark_theme
    '''
    name = 'DarkThemeForm'
"""


class ThemebleTestCase(TestCase):
    """ TestCases for `django_vest.decorators.themeble` decorator.
    """
    @override_settings(CURRENT_THEME='main_theme', DEFAULT_THEME='main_theme')
    def test_default_theme(self):
        """ Default theme is used.
        """
        context = {'themeble': themeble}
        exec(code_template, context)

        self.assertEqual(context['Form'], context['DefaultForm'])

    @override_settings(CURRENT_THEME='dark_theme', DEFAULT_THEME='main_theme')
    def test_dark_theme(self):
        """ Second theme is used.
        """
        context = {'themeble': themeble}
        exec(code_template, context)

        self.assertEqual(context['Form'], context['DarkThemeForm'])

    @override_settings(CURRENT_THEME='unknow', DEFAULT_THEME='main_theme')
    def test_unknow_current_theme(self):
        """ Testing of behavior with invalid `CURRENT_THEME` name.
        """
        context = {'themeble': themeble}
        exec(code_template, context)

        self.assertEqual(context['Form'], context['DefaultForm'])

    @override_settings(CURRENT_THEME='unknow', DEFAULT_THEME='unknow')
    def test_unknow_all_themes(self):
        """ Testing of behavior with invalid themes names.
        """
        context = {'themeble': themeble}
        exec(code_template, context)

        self.assertEqual(context['Form'], context['DefaultForm'])

    @override_settings(CURRENT_THEME=None, DEFAULT_THEME=None)
    def test_themes_not_set(self):
        context = {'themeble': themeble}
        exec(code_template, context)

        self.assertEqual(context['Form'], context['DefaultForm'])

    @override_settings(CURRENT_THEME='dark_theme', DEFAULT_THEME='main_theme')
    def test_failed_to_override_existing_name(self):
        context = {'themeble': themeble}

        with self.assertRaises(RuntimeError):
            exec(invalid_code, context)
