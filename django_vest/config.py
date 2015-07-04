# coding: utf-8
import os

from django.conf import settings as django_settings


class Settings(object):
    """ Simple wrapper for receive settings
    """
    def __getattr__(self, name):
        return getattr(django_settings, name)

    @property
    def CURRENT_THEME(self):
        """ Trying to getting `CURRENT_THEME` parameter
        from settings or os env.
        """
        value = getattr(django_settings, 'CURRENT_THEME', None)
        if value:
            return value
        return os.getenv('CURRENT_THEME', None)

    @property
    def DEFAULT_THEME(self):
        return getattr(django_settings, 'DEFAULT_THEME', None)

settings = Settings()
