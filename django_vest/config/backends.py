# coding: utf-8
from __future__ import unicode_literals
import os

from django.conf import settings as django_settings
from django.utils.functional import cached_property

from django_vest.fields import get_field


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


class Database(object):
    """ Receive `CURRENT_THEME` for db field (django_vest.fields.VestField).
    """
    @property
    def CURRENT_THEME(self):
        field = get_field()
        settings = field.model.objects.first()
        if settings:
            return getattr(settings, field.name)


simple = Simple()
env = Env()
database = Database()
