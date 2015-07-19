# coding: utf-8
from django.test import override_settings
from django.core.urlresolvers import reverse

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


class OnlyForTestCase(TestCase):
    """ TestCases for `django_vest.decorators.only_for` decorator.
    """
    urls_names = ['dark_index', 'dark_index_not_found']

    @override_settings(CURRENT_THEME='main_theme', DEFAULT_THEME='main_theme')
    def test_restict_access_redirect(self):
        """ Test for `dark_index` page.
        """
        url = reverse(self.urls_names[0])
        response = self.client.get(url)
        self.assertRedirects(
            response,
            '{}?next={}'.format(reverse('restict_access'), url))

    @override_settings(CURRENT_THEME='main_theme', DEFAULT_THEME='main_theme')
    def test_dark_index_not_found(self):
        """ Test for raising error
        """
        url = reverse(self.urls_names[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @override_settings(CURRENT_THEME='dark_theme', DEFAULT_THEME='main_theme')
    def test_pages_opened(self):
        """ With right theme all page opened.
        """
        for url in self.urls_names:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)

    @override_settings(CURRENT_THEME=None, DEFAULT_THEME='main_theme')
    def test_pages_opened_without_themes(self):
        """ Without CURRENT_THEME opened default template inside in root
        templates directory.
        """
        for url in self.urls_names:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)
