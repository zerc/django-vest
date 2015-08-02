# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from django_vest.fields import VestField


@python_2_unicode_compatible
class BlogPost(models.Model):
    title = models.CharField('title', max_length=255)

    lead = models.TextField('lead')
    body = models.TextField('body')

    class Meta:
        verbose_name = 'blog post'
        verbose_name_plural = 'blog posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class BlogSettings(models.Model):
    """ Simple model for store common blog settings.
    """
    title = models.CharField('title', max_length=255)

    current_theme = VestField()

    class Meta:
        verbose_name = 'blog settings'
        verbose_name_plural = 'blog settings'

    def __str__(self):
        return self.title
