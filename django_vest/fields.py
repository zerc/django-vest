# coding: utf-8
from __future__ import unicode_literals
from collections import defaultdict

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import force_text

from .utils import get_available_themes

USAGE_CACHE = {}


def get_field():
    try:
        m_name, f_name = [(m, f) for m, f in USAGE_CACHE.items()][0]
    except (IndexError, ValueError):
        return None

    return (models.get_model(*m_name.split('.'))
                  ._meta.get_field_by_name(f_name)[0])


class TrackUsageFieldMixin(object):
    """ Mixin for tracking usage of field.
    """
    def contribute_to_class(self, cls, name, *args, **kwargs):
        # Registering field if he not abstract
        if not cls._meta.abstract:
            key = '{0.app_label}.{0.model_name}'.format(cls._meta)
            USAGE_CACHE[key] = name

            if len(USAGE_CACHE.keys()) > 1:
                raise ImproperlyConfigured('VestField must by only one')

        return super(TrackUsageFieldMixin, self).contribute_to_class(
            cls, name, *args, **kwargs)


class VestField(TrackUsageFieldMixin, models.CharField):
    """ Field for store information about CURRENT_THEME.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 125)
        available_themes = list(get_available_themes())

        choices = kwargs.get('choices', None)
        if choices is None:
            kwargs['choices'] = zip(available_themes, available_themes)
        else:
            diff = (set(force_text(t[0]) for t in choices) -
                    set(available_themes))
            if diff:
                raise ImproperlyConfigured(
                    'VestField got unknow themes: {}'.format(force_text(diff)))

        super(VestField, self).__init__(*args, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_vest\.fields\.VestField"])
except ImportError:
    pass
