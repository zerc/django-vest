# coding: utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^dark/$', views.dark_theme_page, name='dark_index'),
    url(r'^dark2/$', views.dark_theme_page_not_found,
        name='dark_index_not_found'),
    url(r'^restict/$', views.restict_access, name='restict_access'),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
