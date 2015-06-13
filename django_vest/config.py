# coding: utf-8
from django.conf import settings as django_settings


class Settings(object):
    """ Simple proxy above global settings of project.
    """
    def __getattr__(self, name):
        return getattr(django_settings, name)

    @property
    def CURRENT_THEME(self):
        return getattr(django_settings, 'CURRENT_THEME', None)

    @property
    def DEFAULT_THEME(self):
        return getattr(django_settings, 'DEFAULT_THEME', None)

settings = Settings()
