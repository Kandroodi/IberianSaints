from django.forms import ModelForm
from django import forms

from .models import *
from crispy_forms.helper import FormHelper
from django_select2 import forms as s2forms


# Widgets
class SaintTypeWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class ExternalLinkWidget(s2forms.ModelSelect2Widget):
    search_fields = ['link__icontains']


# Forms
class SaintForm(forms.ModelForm):
    class Meta:
        model = Saint
        fields = '__all__'
        widgets = {
            "type": SaintTypeWidget,
            "external_link": ExternalLinkWidget,
        }

    def __init__(self, *args, **kwargs):
        super(SaintForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = False


class ChurchForm(ModelForm):
    class Meta:
        model = Church
        fields = '__all__'
        # its possible to use following line for all fields, also exclude
        # fields = '__all__'
        labels = {
            'name': 'Church Name'
        }

    def __init__(self, *args, **kwargs):
        super(ChurchForm, self).__init__(*args, **kwargs)
        # self.fields['country'].empty_label = "Select"
        self.fields['bibliography'].required = False
        self.fields['institution_type'].required = False
        self.helper = FormHelper()


class BibliographyForm(ModelForm):
    class Meta:
        model = Bibliography
        fields = '__all__'
        # its possible to use following line for all fields, also exclude
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BibliographyForm, self).__init__(*args, **kwargs)
        # self.fields['country'].empty_label = "Select"
        self.fields['year'].required = False


class InstitutionTypeForm(ModelForm):
    class Meta:
        model = InstitutionType
        fields = '__all__'
