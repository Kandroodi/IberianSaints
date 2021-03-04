from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.utils.decorators import method_decorator

from django.views.generic import (View, TemplateView, ListView,
                                  DetailView, CreateView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from utilities.views import edit_model



# Create your views here.

def home(request):
    return render(request, 'saints/home.html')


def edit_church(request, pk=None, focus='', view='complete'):
    names = 'churchsaint_formset,churchobject_formset,churchliturgicalmanuscript_formset'
    return edit_model(request, __name__, 'Church', 'saints', pk, formset_names=names,
                      focus=focus, view=view)


def churchCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ChurchForm()
        else:
            church = Church.objects.get(pk=id)
            form = ChurchForm(instance=church)
        return render(request, 'saints/church_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = ChurchForm(request.POST)
        else:
            church = Church.objects.get(pk=id)
            form = ChurchForm(request.POST, instance=church)
        if form.is_valid():
            form.save()
        return redirect('saints:church-list')  # after save redirect to the city list


def churchList(request):
    context = {'church_list': Church.objects.all()}
    return render(request, 'saints/church_list.html', context)

def churchDelete(request, id):
    city = get_object_or_404(Church, pk=id)
    city.delete()
    return redirect('saints:church-list')


def bibliographyCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = BibliographyForm()
        else:
            bibliography = Bibliography.objects.get(pk=id)
            form = BibliographyForm(instance=bibliography)
        return render(request, 'saints/bibliography_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = BibliographyForm(request.POST)
        else:
            bibliography = Bibliography.objects.get(pk=id)
            form = BibliographyForm(request.POST, instance=bibliography)
        if form.is_valid():
            form.save()
        return redirect('saints:bibliography-list')  # after save redirect to the city list


def bibliographyList(request):
    context = {'bibliography_list': Bibliography.objects.all()}
    return render(request, 'saints/bibliography_list.html', context)

def bibliographyDelete(request, id):
    city = get_object_or_404(Church, pk=id)
    city.delete()
    return redirect('saints:bibliography-list')

def institutionTypeCreate(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = InstitutionTypeForm()
        else:
            institutionType = InstitutionType.objects.get(pk=id)
            form = InstitutionTypeForm(instance=institutionType)
        return render(request, 'saints/institutionType_form.html', {'form': form})
    else:  # request.method == "POST":
        if id == 0:
            form = InstitutionTypeForm(request.POST)
        else:
            institutionType = InstitutionType.objects.get(pk=id)
            form = InstitutionTypeForm(request.POST, instance=institutionType)
        if form.is_valid():
            form.save()
        return redirect('saints:institutionType-list')  # after save redirect to the city list


def institutionTypeList(request):
    context = {'institutionType_list': InstitutionType.objects.all()}
    return render(request, 'saints/institutionType_list.html', context)

def institutionTypeDelete(request, id):
    city = get_object_or_404(Church, pk=id)
    city.delete()
    return redirect('saints:institutionType-list')


# Class Based Views
#-----------------------------------------------------------------------------------------------------------------------
# @method_decorator(login_required, name='dispatch')
class InscriptionListView(ListView):
    model = Inscription
    template_name = 'installations/inscription_list.html'
    context_object_name = 'inscriptions'


# @method_decorator(login_required, name='dispatch')
class InscriptionCreatView(CreateView):
    model = Inscription
    fields = '__all__'
    template_name = 'saints/inscription_form.html'
    success_url = reverse_lazy('saints:inscription-list')


# @method_decorator(login_required, name='dispatch')
class InscriptionUpdateView(UpdateView):
    model = Inscription
    fields = '__all__'
    success_url = reverse_lazy('saints:inscription-list')


# @method_decorator(login_required, name='dispatch')
class InscriptionDeleteView(DeleteView):
    model = Inscription
    success_url = reverse_lazy("saints:inscription-list")

# Saint
# @method_decorator(login_required, name='dispatch')
class SaintListView(ListView):
    model = Saint
    template_name = 'installations/saint_list.html'
    context_object_name = 'saints'


def edit_saint(request, pk=None, focus='', view='complete'):
    names = 'saintchurch_formset,saintinscription_formset,saintobject_formset,saintliturgicalmanuscript_formset'
    return edit_model(request, __name__, 'Saint', 'saints', pk, formset_names=names,
                      focus=focus, view=view)




# @method_decorator(login_required, name='dispatch')
class SaintCreatView(CreateView):
    model = Saint
    form_class = SaintForm
    template_name = 'saints/add_saint.html'
    success_url = reverse_lazy('saints:saint-list')


# @method_decorator(login_required, name='dispatch')
class SaintUpdateView(UpdateView):
    model = Saint
    fields = '__all__'
    success_url = reverse_lazy('saints:saint-list')


# @method_decorator(login_required, name='dispatch')
class SaintDeleteView(DeleteView):
    model = Saint
    success_url = reverse_lazy("saints:saint-list")

# Object
# @method_decorator(login_required, name='dispatch')
class ObjectListView(ListView):
    model = Object
    template_name = 'installations/object_list.html'
    context_object_name = 'objects'


# @method_decorator(login_required, name='dispatch')
class ObjectCreatView(CreateView):
    model = Object
    fields = '__all__'
    template_name = 'saints/object_form.html'
    success_url = reverse_lazy('saints:object-list')


# @method_decorator(login_required, name='dispatch')
class ObjectUpdateView(UpdateView):
    model = Object
    fields = '__all__'
    success_url = reverse_lazy('saints:object-list')


# @method_decorator(login_required, name='dispatch')
class ObjectDeleteView(DeleteView):
    model = Object
    success_url = reverse_lazy("saints:object-list")


# Feast
# @method_decorator(login_required, name='dispatch')
class FeastListView(ListView):
    model = Feast
    template_name = 'installations/feast_list.html'
    context_object_name = 'feasts'


# @method_decorator(login_required, name='dispatch')
class FeastCreatView(CreateView):
    model = Feast
    fields = '__all__'
    template_name = 'saints/feast_form.html'
    success_url = reverse_lazy('saints:feast-list')


# @method_decorator(login_required, name='dispatch')
class FeastUpdateView(UpdateView):
    model = Feast
    fields = '__all__'
    success_url = reverse_lazy('saints:feast-list')


# @method_decorator(login_required, name='dispatch')
class FeastDeleteView(DeleteView):
    model = Feast
    success_url = reverse_lazy("saints:feast-list")


# LiturgicalManuscript
# @method_decorator(login_required, name='dispatch')
class LiturgicalManuscriptListView(ListView):
    model = LiturgicalManuscript
    template_name = 'installations/liturgicalmanuscript_list.html'
    context_object_name = 'liturgicalmanuscripts'


# @method_decorator(login_required, name='dispatch')
class LiturgicalManuscriptCreatView(CreateView):
    model = LiturgicalManuscript
    fields = '__all__'
    template_name = 'saints/liturgicalmanuscript_form.html'
    success_url = reverse_lazy('saints:liturgicalmanuscript-list')


# @method_decorator(login_required, name='dispatch')
class LiturgicalManuscriptUpdateView(UpdateView):
    model = LiturgicalManuscript
    fields = '__all__'
    success_url = reverse_lazy('saints:liturgicalmanuscript-list')


# @method_decorator(login_required, name='dispatch')
class LiturgicalManuscriptDeleteView(DeleteView):
    model = LiturgicalManuscript
    success_url = reverse_lazy("saints:liturgicalmanuscript-list")


# Rite
# @method_decorator(login_required, name='dispatch')
class RiteListView(ListView):
    model = Rite
    template_name = 'installations/rite_list.html'
    context_object_name = 'rites'


# @method_decorator(login_required, name='dispatch')
class RiteCreatView(CreateView):
    model = Rite
    fields = '__all__'
    template_name = 'saints/rite_form.html'
    success_url = reverse_lazy('saints:rite-list')


# @method_decorator(login_required, name='dispatch')
class RiteUpdateView(UpdateView):
    model = Rite
    fields = '__all__'
    success_url = reverse_lazy('saints:rite-list')


# @method_decorator(login_required, name='dispatch')
class RiteDeleteView(DeleteView):
    model = Rite
    success_url = reverse_lazy("saints:rite-list")


# ManuscriptType
# @method_decorator(login_required, name='dispatch')
class ManuscriptTypeListView(ListView):
    model = ManuscriptType
    template_name = 'installations/manuscripttype_list.html'
    context_object_name = 'manuscripttypes'


# @method_decorator(login_required, name='dispatch')
class ManuscriptTypeCreatView(CreateView):
    model = ManuscriptType
    fields = '__all__'
    template_name = 'saints/manuscripttype_form.html'
    success_url = reverse_lazy('saints:manuscripttype-list')


# @method_decorator(login_required, name='dispatch')
class ManuscriptTypeUpdateView(UpdateView):
    model = ManuscriptType
    fields = '__all__'
    success_url = reverse_lazy('saints:manuscripttype-list')


# @method_decorator(login_required, name='dispatch')
class ManuscriptTypeDeleteView(DeleteView):
    model = ManuscriptType
    success_url = reverse_lazy("saints:manuscripttype-list")


# ObjectType
# @method_decorator(login_required, name='dispatch')
class ObjectTypeListView(ListView):
    model = ObjectType
    template_name = 'installations/objecttype_list.html'
    context_object_name = 'objecttypes'


# @method_decorator(login_required, name='dispatch')
class ObjectTypeCreatView(CreateView):
    model = ObjectType
    fields = '__all__'
    template_name = 'saints/objecttype_form.html'
    success_url = reverse_lazy('saints:objecttype-list')


# @method_decorator(login_required, name='dispatch')
class ObjectTypeUpdateView(UpdateView):
    model = ObjectType
    fields = '__all__'
    success_url = reverse_lazy('saints:objecttype-list')


# @method_decorator(login_required, name='dispatch')
class ObjectTypeDeleteView(DeleteView):
    model = ObjectType
    success_url = reverse_lazy("saints:objecttype-list")


# SaintType
# @method_decorator(login_required, name='dispatch')
class SaintTypeListView(ListView):
    model = SaintType
    template_name = 'installations/sainttype_list.html'
    context_object_name = 'sainttypes'


# @method_decorator(login_required, name='dispatch')
class SaintTypeCreatView(CreateView):
    model = SaintType
    fields = '__all__'
    template_name = 'saints/sainttype_form.html'
    success_url = reverse_lazy('saints:sainttype-list')


# @method_decorator(login_required, name='dispatch')
class SaintTypeUpdateView(UpdateView):
    model = SaintType
    fields = '__all__'
    success_url = reverse_lazy('saints:sainttype-list')


# @method_decorator(login_required, name='dispatch')
class SaintTypeDeleteView(DeleteView):
    model = SaintType
    success_url = reverse_lazy("saints:sainttype-list")

# ExternalLink
# @method_decorator(login_required, name='dispatch')
class ExternalLinkListView(ListView):
    model = ExternalLink
    template_name = 'installations/externallink_list.html'
    context_object_name = 'externallinks'


# @method_decorator(login_required, name='dispatch')
class ExternalLinkCreatView(CreateView):
    model = ExternalLink
    fields = '__all__'
    template_name = 'saints/externallink_form.html'
    success_url = reverse_lazy('saints:externallink-list')


# @method_decorator(login_required, name='dispatch')
class ExternalLinkUpdateView(UpdateView):
    model = ExternalLink
    fields = '__all__'
    success_url = reverse_lazy('saints:externallink-list')


# @method_decorator(login_required, name='dispatch')
class ExternalLinkDeleteView(DeleteView):
    model = ExternalLink
    success_url = reverse_lazy("saints:externallink-list")


# Location
# @method_decorator(login_required, name='dispatch')
class LocationListView(ListView):
    model = Location
    template_name = 'installations/location_list.html'
    context_object_name = 'locations'


# @method_decorator(login_required, name='dispatch')
class LocationCreatView(CreateView):
    model = Location
    fields = '__all__'
    template_name = 'saints/location_form.html'
    success_url = reverse_lazy('saints:location-list')


# @method_decorator(login_required, name='dispatch')
class LocationUpdateView(UpdateView):
    model = Location
    fields = '__all__'
    success_url = reverse_lazy('saints:location-list')


# @method_decorator(login_required, name='dispatch')
class LocationDeleteView(DeleteView):
    model = Location
    success_url = reverse_lazy("saints:location-list")


# InstitutionType
# @method_decorator(login_required, name='dispatch')
class InstitutionTypeListView(ListView):
    model = InstitutionType
    template_name = 'installations/institutiontype_list.html'
    context_object_name = 'institutiontypes'


# @method_decorator(login_required, name='dispatch')
class InstitutionTypeCreatView(CreateView):
    model = InstitutionType
    fields = '__all__'
    template_name = 'saints/institutiontype_form.html'
    success_url = reverse_lazy('saints:institutiontype-list')


# @method_decorator(login_required, name='dispatch')
class InstitutionTypeUpdateView(UpdateView):
    model = InstitutionType
    fields = '__all__'
    success_url = reverse_lazy('saints:institutiontype-list')


# @method_decorator(login_required, name='dispatch')
class InstitutionTypeDeleteView(DeleteView):
    model = InstitutionType
    success_url = reverse_lazy("saints:institutiontype-list")
