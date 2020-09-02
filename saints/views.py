from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.utils.decorators import method_decorator

from django.views.generic import (View, TemplateView, ListView,
                                  DetailView, CreateView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy


# Create your views here.

def home(request):
    return render(request, 'saints/home.html')


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

