# coding: utf-8
from django.http import Http404
from django.views.generic.base import TemplateView

from django_vest import only_for

from forms import FormOne


class IndexPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexPage, self).get_context_data(*args, **kwargs)
        context['form_one'] = FormOne()
        return context


dark_theme_page = only_for('dark_theme', redirect_to='restict_access')(
    TemplateView.as_view(template_name='dark_theme_page.html'))

dark_theme_page_not_found = \
    only_for('dark_theme', raise_error=Http404)(
        TemplateView.as_view(template_name='dark_theme_page.html'))


restict_access = TemplateView.as_view(template_name='restict_access.html')
