# coding: utf-8
from django.test import override_settings
from django.contrib.auth import get_user_model
from django.template.base import TemplateDoesNotExist
from django.core.urlresolvers import reverse_lazy

from django_vest.test import TestCase
from django_vest.templates_loaders import DJANGO_ORIGIN


class TemplateLoaderTestCase(TestCase):
    @override_settings(CURRENT_THEME='main_theme', DEFAULT_THEME='main_theme')
    def test_default_theme(self):
        """ Default theme is used. Index page opened.
        Dont have are parent.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        templates = get_templates_used(response)
        self.assertEqual(len(templates), 1)
        self.assertIn('index.html', templates)

    @override_settings(CURRENT_THEME='dark_theme', DEFAULT_THEME='main_theme')
    def test_dark_theme(self):
        """ Second theme is used. Index page opened.
        Must be extended from default theme index.html.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        templates = get_templates_used(response)
        self.assertEqual(len(templates), 2)
        self.assertIn('index.html', templates)
        self.assertIn('DEFAULT_THEME/index.html', templates)

    @override_settings(CURRENT_THEME='unknow', DEFAULT_THEME='main_theme')
    def test_unknow_current_theme(self):
        """ Testing of behavior with invalid `CURRENT_THEME` name.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        templates = get_templates_used(response)
        self.assertEqual(len(templates), 1)
        self.assertIn('index.html', templates)

    @override_settings(CURRENT_THEME='unknow', DEFAULT_THEME='unknow')
    def test_unknow_all_themes(self):
        """ Testing of behavior with invalid themes names.
        """
        self.assertRaises(TemplateDoesNotExist, lambda: self.client.get('/'))

    @override_settings(CURRENT_THEME=None, DEFAULT_THEME=None)
    def test_themes_not_set(self):
        self.assertRaises(TemplateDoesNotExist, lambda: self.client.get('/'))


class AppsTemplateLoaderTestCase(TestCase):
    """ TestCase for `django_vest.template_loaders.AppsLoader`
    """
    url = reverse_lazy('admin:auth_user_changelist')

    @classmethod
    def setUpClass(cls):
        cls.User = get_user_model()
        cls.username = cls.password = 'user'
        cls.email = 'user@users.com'

        cls.user = cls.User.objects.create_superuser(cls.username, cls.email,
                                                     cls.password)

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    def test_override_origin_template(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        templates = get_templates_used(response)

        self.assertIn(DJANGO_ORIGIN, ','.join(templates))
        self.assertIn('Template has been overridden', response.content)


def get_templates_used(response):
    return [t.name for t in response.templates
            if t.name is not None]
