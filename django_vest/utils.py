# coding: utf-8
from __future__ import unicode_literals

from importlib import import_module


def load_object(s):
    """ Load backend by dotted path.
    """
    try:
        m_path, o_name = s.rsplit('.', 1)
    except ValueError:
        raise ImportError('Cant import backend from path: {}'.format(s))

    module = import_module(m_path)
    return getattr(module, o_name)
