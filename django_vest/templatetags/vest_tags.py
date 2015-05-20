# coding: utf-8
from django import template, forms

from django_vest import config

register = template.Library()


@register.filter
def themeble(value):
    """ Replace the keyword in the `value` on the name of active theme.

    Example:
        {% static 'img/THEME/logo.png'|themeble %} ==
        {% static 'img/cool_theme/logo.png' %}
        # if CURRENT_THEME == 'cool_theme'
    """
    return (value.replace('THEME', config.CURRENT_THEME or '')
                 .replace('DEFAULT_THEME', config.DEFAULT_THEME or ''))
