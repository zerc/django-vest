# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import BlogPost, BlogSettings


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title', 'lead', 'body', 'mutli_field')

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register([BlogSettings])
