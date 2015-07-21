# coding: utf-8
import os

from django.test import override_settings
from django.contrib.auth import get_user_model
from django.template.base import TemplateDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.text import force_text

import mock

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
        self._check_is_dark_theme()

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

    @override_settings(CURRENT_THEME=None, DEFAULT_THEME='main_theme')
    def test_gettings_theme_from_env(self):
        """ Testing for getting param from os env
        """
        with mock.patch.dict('os.environ',
                             {'DJANGO_VEST_CURRENT_THEME': 'dark_theme'}):
            self._check_is_dark_theme()

    def _check_is_dark_theme(self):
        """ Common checks for `dark_theme`
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        templates = get_templates_used(response)
        self.assertEqual(len(templates), 2)
        self.assertIn('index.html', templates)
        self.assertIn('DEFAULT_THEME/index.html', templates)


class AppsTemplateLoaderTestCase(TestCase):
    """ TestCase for `django_vest.template_loaders.AppsLoader`
    """
    @classmethod
    def setUpClass(cls):
        super(AppsTemplateLoaderTestCase, cls).setUpClass()

        cls.User = get_user_model()
        cls.username = cls.password = 'user'
        cls.email = 'user@users.com'

        cls.user = cls.User.objects.create_superuser(cls.username, cls.email,
                                                     cls.password)

        cls.url = reverse('admin:auth_user_changelist')

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    def test_override_origin_template(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        templates = get_templates_used(response)

        self.assertIn(DJANGO_ORIGIN, ','.join(templates))
        self.assertIn(u'Template has been overridden',
                      force_text(response.content))


def get_templates_used(response):
    return [t.name for t in response.templates
            if t.name is not None]
