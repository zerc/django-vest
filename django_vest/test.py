# coding: utf-8
""" Some common things for tests.
"""
import unittest

from django.test import TestCase as BaseTestCase
from django.test.runner import DiscoverRunner as BaseTestRunner

from django_vest import config


class ThemebleTestSuite(unittest.TestSuite):
    """ Skip casess with countTestCases == 0.
    """
    def __init__(self, tests=()):
        tests = [t for t in tests if t.countTestCases()]
        super(ThemebleTestSuite, self).__init__(tests)

    def addTest(self, test):
        if test.countTestCases():
            super(ThemebleTestSuite, self).addTest(test)


class ThemebleTestLoader(unittest.TestLoader):
    suiteClass = ThemebleTestSuite

themebleTestLoader = ThemebleTestLoader()


class ThemebleTestRunner(BaseTestRunner):
    """ Our custom TestRunner.
    Set in your settings.py:

        ``TEST_RUNNER = 'django_vest.test.ThemebleTestRunner'``
    """
    test_suite = ThemebleTestSuite
    test_loader = themebleTestLoader

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if self.verbosity > 1:
            print(u'>>> Run tests for theme: {}'.format(
                config.CURRENT_THEME))
        return super(ThemebleTestRunner, self).run_tests(
            test_labels, extra_tests, **kwargs)


class TestCase(BaseTestCase):
    """ Our new base TestCase.
    """
    # List of themes
    THEMES = None

    def countTestCases(self):
        themes = self.THEMES or []

        if not isinstance(themes, (list, tuple, set)):
            themes = [themes]

        if not themes or config.CURRENT_THEME in themes:
            return super(TestCase, self).countTestCases()

        return 0
