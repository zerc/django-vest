# coding: utf-8
from django.test import override_settings
from django.template.base import TemplateDoesNotExist

from django_vest.test import TestCase


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
        """ Test bahavior with invalid `CURRENT_THEME` name.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        templates = get_templates_used(response)
        self.assertEqual(len(templates), 1)
        self.assertIn('index.html', templates)

    @override_settings(CURRENT_THEME='unknow', DEFAULT_THEME='unknow')
    def test_unknow_current_theme(self):
        """ Test bahavior with invalid themes names.
        """
        self.assertRaises(TemplateDoesNotExist, lambda: self.client.get('/'))

    @override_settings(CURRENT_THEME=None, DEFAULT_THEME=None)
    def test_themes_not_set(self):
        self.assertRaises(TemplateDoesNotExist, lambda: self.client.get('/'))


def get_templates_used(response):
    return [t.name for t in response.templates
            if t.name is not None]
