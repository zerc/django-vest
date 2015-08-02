# coding: utf-8
from __future__ import unicode_literals

import os

from django.conf import settings as django_settings

from django_vest.utils import load_object


class SettingsLoader(object):
    """ Use backends from 'VEST_SETTINGS_BACKENDS_LIST'
    for getting settings.
    """
    def __init__(self):
        self.backends_list = getattr(django_settings,
                                     'VEST_SETTINGS_BACKENDS_LIST',
                                     ('django_vest.config.backends.simple',
                                      'django_vest.config.backends.env'))
        self.backends = [load_object(b) for b in self.backends_list]

    def __getattr__(self, name):
        for b in self.backends:
            value = getattr(b, name, None)
            if value:
                return value

settings = SettingsLoader()
