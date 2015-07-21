# coding: utf-8
from __future__ import unicode_literals
import os

from django.conf import settings as django_settings


class Simple(object):
    """ Simple wrapper around settings file.
    """
    source = django_settings

    def __getattr__(self, name):
        return getattr(self.source, name)

    @property
    def CURRENT_THEME(self):
        """ Trying to getting `CURRENT_THEME` parameter
        from settings or os env.
        """
        return getattr(self.source, 'CURRENT_THEME', None)

    @property
    def DEFAULT_THEME(self):
        return getattr(self.source, 'DEFAULT_THEME', None)


class Env(object):
    """ Receive settings for OS env.
    """
    @property
    def CURRENT_THEME(self):
        """ Trying to getting `CURRENT_THEME` parameter
        from settings or os env.
        """
        return os.environ.get('DJANGO_VEST_CURRENT_THEME', None)

    @property
    def DEFAULT_THEME(self):
        return os.environ.get('DJANGO_VEST_DEFAULT_THEME', None)


simple = Simple()
env = Env()
