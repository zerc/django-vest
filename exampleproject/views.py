# coding: utf-8
from django.views.generic.base import TemplateView

from forms import FormOne


class IndexPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexPage, self).get_context_data(*args, **kwargs)
        context['form_one'] = FormOne()
        return context
