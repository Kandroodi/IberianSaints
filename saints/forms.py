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

    type = forms.ModelChoiceField(
        queryset=SaintType.objects.all().order_by('name'),
        # this line refreshes the list when a new item is entered using the plus button
        widget=SaintTypeWidget(
            attrs={'data-placeholder': 'Select saint type',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)

    external_link = forms.ModelChoiceField(
        queryset=ExternalLink.objects.all().order_by('link'),
        # this line refreshes the list when a new item is entered using the plus button
        widget=ExternalLinkWidget(
            attrs={'data-placeholder': 'Select external link',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:100%', 'rows': 3}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(SaintForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
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
