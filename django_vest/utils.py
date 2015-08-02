# coding: utf-8
from __future__ import unicode_literals
import os
from importlib import import_module

from django.conf import settings

is_theme_dir = lambda d: d.endswith('_theme')


def load_object(s):
    """ Load backend by dotted path.
    """
    try:
        m_path, o_name = s.rsplit('.', 1)
    except ValueError:
        raise ImportError('Cant import backend from path: {}'.format(s))

    module = import_module(m_path)
    return getattr(module, o_name)


def get_available_themes():
    """ Iterator on available themes
    """
    for d in settings.TEMPLATE_DIRS:
        for _d in os.listdir(d):
            if os.path.isdir(os.path.join(d, _d)) and is_theme_dir(_d):
                yield _d
