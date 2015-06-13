# coding: utf-8
from django.test import override_settings

from django_vest.test import TestCase
from django_vest.decorators import themeble

code_template = """
@themeble(name='Form', themes=('dark_theme',), global_context=globals())
class DarkThemeForm(object):
    ''' Some kind of logic for dark_theme
    '''
    name = 'DarkThemeForm'


@themeble(name='Form', global_context=globals())
class DefaultForm(object):
    ''' Default logic for all themes
    '''
    name = 'Default form'
"""


class ThemebleTestCase(TestCase):
    """ TestCases for `django_vest.decorators.themeble` decorator.
    """
    @override_settings(CURRENT_THEME='main_theme', DEFAULT_THEME='main_theme')
    def test_default_theme(self):
        """ Default theme is used.
        """
        context = {'themeble': themeble}
        exec code_template in context

        self.assertEqual(context['Form'], context['DefaultForm'])

    @override_settings(CURRENT_THEME='dark_theme', DEFAULT_THEME='main_theme')
    def test_dark_theme(self):
        """ Second theme is used.
        """
        context = {'themeble': themeble}
        exec code_template in context

        self.assertEqual(context['Form'], context['DarkThemeForm'])
