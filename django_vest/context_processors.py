# coding: utf-8
from django_vest.config import settings


def add_theme_info(request):
    return dict(CURRENT_THEME=settings.CURRENT_THEME,
                DEFAULT_THEME=settings.DEFAULT_THEME)
