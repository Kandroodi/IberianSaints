from django.forms import ModelForm, inlineformset_factory
from django import forms

from .models import *
from crispy_forms.helper import FormHelper
from django_select2 import forms as s2forms


# Widgets
class SaintTypeWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class SaintWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class ChurchWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class InscriptionWidget(s2forms.ModelSelect2Widget):
    search_fields = ['reference_no__icontains']


class ObjectWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class ObjectTypeWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class LiturgicalManuscriptWidget(s2forms.ModelSelect2Widget):
    search_fields = ['shelf_no__icontains']


class ExternalLinkWidget(s2forms.ModelSelect2Widget):
    search_fields = ['link__icontains']


class CoordinatesWidget(s2forms.ModelSelect2Widget):
    search_fields = ['latitude__icontains',
                     'longitude__icontains',
                     ]


class InstitutionTypeWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class RiteWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class FeastWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class ManuscriptTypeWidget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']


class BibliographyWidget(s2forms.ModelSelect2Widget):
    search_fields = ['short_title__icontains']


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
        labels = {
            'name': 'Church Name'
        }

    start_date_lower = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter lower bound'}))
    start_date_upper = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter upper bound'}))
    end_date_lower = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter lower bound'}))
    end_date_upper = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter upper bound'}))
    coordinates = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        # this line refreshes the list when a new item is entered using the plus button
        widget=CoordinatesWidget(
            attrs={'data-placeholder': 'Select coordinates',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    institution_type = forms.ModelChoiceField(
        queryset=InstitutionType.objects.all(),
        # this line refreshes the list when a new item is entered using the plus button
        widget=InstitutionTypeWidget(
            attrs={'data-placeholder': 'Select institution type',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)

    bibliography = forms.ModelChoiceField(
        queryset=Bibliography.objects.all(),
        # this line refreshes the list when a new item is entered using the plus button
        widget=BibliographyWidget(
            attrs={'data-placeholder': 'Select bibliography',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:100%', 'rows': 3}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(ChurchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['start_date_lower'].required = False
        self.fields['start_date_upper'].required = False
        self.fields['end_date_lower'].required = False
        self.fields['end_date_upper'].required = False


class ObjectForm(ModelForm):
    class Meta:
        model = Object
        fields = '__all__'

    date_lower = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter lower bound'}))
    date_upper = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter upper bound'}))
    original_location = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        widget=ChurchWidget(
            attrs={'data-placeholder': 'Select original location',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    current_location = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        widget=ChurchWidget(
            attrs={'data-placeholder': 'Select current location',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    type = forms.ModelChoiceField(
        queryset=ObjectType.objects.all().order_by('name'),
        widget=ObjectTypeWidget(
            attrs={'data-placeholder': 'Select object type',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)

    bibliography = forms.ModelChoiceField(
        queryset=Bibliography.objects.all(),
        widget=BibliographyWidget(
            attrs={'data-placeholder': 'Select bibliography',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:100%', 'rows': 3}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(ObjectForm, self).__init__(*args, **kwargs)
        self.fields['date_lower'].required = False
        self.fields['date_upper'].required = False


class InscriptionForm(ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'

    date_lower = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter lower bound'}))
    date_upper = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter upper bound'}))

    original_location = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        widget=ChurchWidget(
            attrs={'data-placeholder': 'Select original location',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)

    bibliography = forms.ModelChoiceField(
        queryset=Bibliography.objects.all(),
        widget=BibliographyWidget(
            attrs={'data-placeholder': 'Select bibliography',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    text = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:100%', 'rows': 3}),
        required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:100%', 'rows': 3}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        self.fields['date_lower'].required = False
        self.fields['date_upper'].required = False


class LiturgicalManuscriptForm(ModelForm):
    class Meta:
        model = LiturgicalManuscript
        fields = '__all__'

    date_lower = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter lower bound'}))
    date_upper = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter upper bound'}))

    rite = forms.ModelChoiceField(
        queryset=Rite.objects.all(),
        widget=RiteWidget(
            attrs={'data-placeholder': 'Select rite',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    type = forms.ModelChoiceField(
        queryset=ManuscriptType.objects.all(),
        widget=ManuscriptTypeWidget(
            attrs={'data-placeholder': 'Select manuscript type',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    provenance = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        widget=ChurchWidget(
            attrs={'data-placeholder': 'Select provenance',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    feast = forms.ModelChoiceField(
        queryset=Rite.objects.all(),
        widget=FeastWidget(
            attrs={'data-placeholder': 'Select feast',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    external_link = forms.ModelChoiceField(
        queryset=ExternalLink.objects.all().order_by('link'),
        widget=ExternalLinkWidget(
            attrs={'data-placeholder': 'Select external link',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    bibliography = forms.ModelChoiceField(
        queryset=Bibliography.objects.all(),
        widget=BibliographyWidget(
            attrs={'data-placeholder': 'Select bibliography',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
        required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:100%', 'rows': 3}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(LiturgicalManuscriptForm, self).__init__(*args, **kwargs)
        self.fields['date_lower'].required = False
        self.fields['date_upper'].required = False

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


# Relations form
class SaintChurchRelationForm(ModelForm):
    saint = forms.ModelChoiceField(
        queryset=Saint.objects.all(),
        widget=SaintWidget(
            attrs={'data-placeholder': 'Select saint',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    church = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        widget=ChurchWidget(
            attrs={'data-placeholder': 'Select church',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    class Meta:
        model = SaintChurchRelation
        fields = ('saint', 'church')


class SaintInscriptionRelationForm(ModelForm):
    saint = forms.ModelChoiceField(
        queryset=Saint.objects.all(),
        widget=SaintWidget(
            attrs={'data-placeholder': 'Select saint',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )
    inscription = forms.ModelChoiceField(
        queryset=Inscription.objects.all(),
        widget=InscriptionWidget(
            attrs={'data-placeholder': 'Select inscription',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    class Meta:
        model = SaintInscriptionRelation
        fields = ('saint', 'inscription')


class SaintObjectRelationForm(ModelForm):
    saint = forms.ModelChoiceField(
        queryset=Saint.objects.all(),
        widget=SaintWidget(
            attrs={'data-placeholder': 'Select saint',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    object = forms.ModelChoiceField(
        queryset=Object.objects.all(),
        widget=ObjectWidget(
            attrs={'data-placeholder': 'Select object',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    class Meta:
        model = SaintObjectRelation
        fields = ('saint', 'object')


class SaintLitManuscriptRelationForm(ModelForm):
    saint = forms.ModelChoiceField(
        queryset=Saint.objects.all(),
        widget=SaintWidget(
            attrs={'data-placeholder': 'Select saint',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    liturgical_manuscript = forms.ModelChoiceField(
        queryset=LiturgicalManuscript.objects.all(),
        widget=LiturgicalManuscriptWidget(
            attrs={'data-placeholder': 'Select liturgical manuscript',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    class Meta:
        model = SaintLitManuscriptRelation
        fields = ('saint', 'liturgical_manuscript')


class ChurchObjectRelationForm(ModelForm):
    church = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        widget=ChurchWidget(
            attrs={'data-placeholder': 'Select church',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    object = forms.ModelChoiceField(
        queryset=Object.objects.all(),
        widget=ObjectWidget(
            attrs={'data-placeholder': 'Select object',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    class Meta:
        model = ObjectChurchRelation
        fields = ('church', 'object', 'start_date', 'end_date')


class ChurchLitManuscriptRelationForm(ModelForm):
    church = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        widget=ChurchWidget(
            attrs={'data-placeholder': 'Select church',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    liturgical_manuscript = forms.ModelChoiceField(
        queryset=LiturgicalManuscript.objects.all(),
        widget=LiturgicalManuscriptWidget(
            attrs={'data-placeholder': 'Select liturgical manuscript',
                   'style': 'width:100%;', 'class': 'searching',
                   'data-minimum-input-length': '1'}),
    )

    class Meta:
        model = LitManuscriptChurchRelation
        fields = ('church', 'liturgical_manuscript', 'start_date', 'end_date')


# Formsets

saintchurch_formset = inlineformset_factory(
    Saint, SaintChurchRelation, form=SaintChurchRelationForm, extra=1)
churchsaint_formset = inlineformset_factory(
    Church, SaintChurchRelation, form=SaintChurchRelationForm, extra=1)

saintinscription_formset = inlineformset_factory(
    Saint, SaintInscriptionRelation, form=SaintInscriptionRelationForm, extra=1)
inscriptionsaint_formset = inlineformset_factory(
    Inscription, SaintInscriptionRelation, form=SaintInscriptionRelationForm, extra=1)

saintobject_formset = inlineformset_factory(
    Saint, SaintObjectRelation, form=SaintObjectRelationForm, extra=1)
objectsaint_formset = inlineformset_factory(
    Object, SaintObjectRelation, form=SaintObjectRelationForm, extra=1)

saintliturgicalmanuscript_formset = inlineformset_factory(
    Saint, SaintLitManuscriptRelation, form=SaintLitManuscriptRelationForm, extra=1)
liturgicalmanuscriptsaint_formset = inlineformset_factory(
    LiturgicalManuscript, SaintLitManuscriptRelation, form=SaintLitManuscriptRelationForm, extra=1)

churchobject_formset = inlineformset_factory(
    Church, ObjectChurchRelation, form=ChurchObjectRelationForm, extra=1)
objectchurch_formset = inlineformset_factory(
    Object, ObjectChurchRelation, form=ChurchObjectRelationForm, extra=1)

churchliturgicalmanuscript_formset = inlineformset_factory(
    Church, LitManuscriptChurchRelation, form=ChurchLitManuscriptRelationForm, extra=1)
liturgicalmanuscriptchurch_formset = inlineformset_factory(
    LiturgicalManuscript, LitManuscriptChurchRelation, form=ChurchLitManuscriptRelationForm, extra=1)
