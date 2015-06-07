# coding: utf-8
from django import forms


class FormOne(forms.Form):
    """ Exmaple form with several types of fields.
    """
    char_field = forms.CharField(label=u'CharField')

    radio_field = forms.ChoiceField(
        widget=forms.RadioSelect,
        label=u'RadioSelect',
        choices=((x, 'choice %s' % x) for x in range(5)),
        help_text=u'Some field help text')

    multiple_select_field = forms.ChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label=u'CheckboxSelectMultiple',
        choices=((x, 'choice %s' % x) for x in range(5)),
        help_text=u'Some field help text'
    )

    checkbox_field = forms.BooleanField(label=u'BooleanField')

    file_field = forms.FileField(label=u'FileField', required=False)
