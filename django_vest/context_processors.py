# coding: utf-8
from django_vest import config


def add_theme_info(request):
    return dict(CURRENT_THEME=config.CURRENT_THEME,
                DEFAULT_THEME=config.DEFAULT_THEME)
