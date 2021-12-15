from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.utils.decorators import method_decorator

from django.views.generic import (View, TemplateView, ListView,
                                  DetailView, CreateView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from utilities.views import edit_model
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from utilities.views import saintsimplesearch, churchsimplesearch, objectsimplesearch


# Create your views here.

def register(request):
    registered = False

    if request.method == 'POST':
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            user.is_active = False
            # Update with Hashed password
            user.save()
            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user
            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
            # Now save model
            profile.save()
            # Registration Successful!
            registered = True
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'saints/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page. In this case their homepage.
                return HttpResponseRedirect(reverse('saints:home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'saints/login.html', {})


@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('saints:home'))


#
def home(request):
    return render(request, 'saints/home.html')


@login_required(login_url='/login/')
def edit_church(request, pk=None, focus='', view='complete'):
    names = 'churchsaint_formset,churchobject_formset,churchinscription_formset,churchliturgicalmanuscript_formset'
    return edit_model(request, __name__, 'Church', 'saints', pk, formset_names=names,
                      focus=focus, view=view)


@login_required(login_url='/login/')
def churchList(request):
    query_set = churchsimplesearch(request, 'saints', 'church')
    query = request.GET.get("q", "")
    context = {'church_list': query_set,
               'nentries': len(query_set),
               'query': query}
    return render(request, 'saints/church_list.html', context)



@login_required(login_url='/login/')
def churchDelete(request, id):
    city = get_object_or_404(Church, pk=id)
    city.delete()
    return redirect('saints:church-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ChurchDetailView(DetailView):
    model = Church


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def bibliographyList(request):
    context = {'bibliography_list': Bibliography.objects.all()}
    return render(request, 'saints/bibliography_list.html', context)


@login_required(login_url='/login/')
def bibliographyDelete(request, id):
    city = get_object_or_404(Church, pk=id)
    city.delete()
    return redirect('saints:bibliography-list')


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def institutionTypeList(request):
    context = {'institutionType_list': InstitutionType.objects.all()}
    return render(request, 'saints/institutionType_list.html', context)


@login_required(login_url='/login/')
def institutionTypeDelete(request, id):
    city = get_object_or_404(Church, pk=id)
    city.delete()
    return redirect('saints:institutionType-list')


# Class Based Views
# -----------------------------------------------------------------------------------------------------------------------
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InscriptionListView(ListView):
    model = Inscription
    template_name = 'installations/inscription_list.html'
    context_object_name = 'inscriptions'


@login_required(login_url='/login/')
def edit_inscription(request, pk=None, focus='', view='complete'):
    names = 'inscriptionsaint_formset,inscriptionchurch_formset'
    return edit_model(request, __name__, 'Inscription', 'saints', pk, formset_names=names,
                      focus=focus, view=view)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InscriptionUpdateView(UpdateView):
    model = Inscription
    fields = '__all__'
    success_url = reverse_lazy('saints:inscription-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InscriptionDeleteView(DeleteView):
    model = Inscription
    success_url = reverse_lazy("saints:inscription-list")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InscriptionDetailView(DetailView):
    model = Inscription


#Saint
@login_required(login_url='/login/')
def SaintList(request):
    query_set = saintsimplesearch(request, 'saints', 'saint')
    query = request.GET.get("q", "")
    # query_set = Installation.objects.all()
    # if query is not None:
    #     query_set = query_set.filter(name__icontains=query)
    context = {'saint_list': query_set,
               'nentries': len(query_set),
               'query': query}
    return render(request, 'saints/saint_list.html', context)


@login_required(login_url='/login/')
def edit_saint(request, pk=None, focus='', view='complete'):
    names = 'saintchurch_formset,saintinscription_formset,saintobject_formset,saintliturgicalmanuscript_formset'
    return edit_model(request, __name__, 'Saint', 'saints', pk, formset_names=names,
                      focus=focus, view=view)


@login_required(login_url='/login/')
class SaintUpdateView(UpdateView):
    model = Saint
    fields = '__all__'
    success_url = reverse_lazy('saints:saint-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SaintDeleteView(DeleteView):
    model = Saint
    success_url = reverse_lazy("saints:saint-list")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SaintDetailView(DetailView):
    model = Saint


# Object
# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class ObjectListView(ListView):
#     model = Object
#     template_name = 'installations/object_list.html'
#     context_object_name = 'objects'
#
#
@login_required(login_url='/login/')
def ObjectList(request):
    query_set = objectsimplesearch(request, 'saints', 'object')
    query = request.GET.get("q", "")
    context = {'object_list': query_set,
               'nentries': len(query_set),
               'query': query}
    return render(request, 'saints/object_list.html', context)


@login_required(login_url='/login/')
def edit_object(request, pk=None, focus='', view='complete'):
    names = 'objectsaint_formset,objectchurch_formset'
    return edit_model(request, __name__, 'Object', 'saints', pk, formset_names=names,
                      focus=focus, view=view)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ObjectUpdateView(UpdateView):
    model = Object
    fields = '__all__'
    success_url = reverse_lazy('saints:object-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ObjectDeleteView(DeleteView):
    model = Object
    success_url = reverse_lazy("saints:object-list")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ObjectDetailView(DetailView):
    model = Object


# Feast
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FeastListView(ListView):
    model = Feast
    template_name = 'installations/feast_list.html'
    context_object_name = 'feasts'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FeastCreatView(CreateView):
    model = Feast
    fields = '__all__'
    template_name = 'saints/feast_form.html'
    success_url = reverse_lazy('saints:feast-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FeastUpdateView(UpdateView):
    model = Feast
    fields = '__all__'
    success_url = reverse_lazy('saints:feast-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FeastDeleteView(DeleteView):
    model = Feast
    success_url = reverse_lazy("saints:feast-list")


# LiturgicalManuscript
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class LiturgicalManuscriptListView(ListView):
    model = LiturgicalManuscript
    template_name = 'installations/liturgicalmanuscript_list.html'
    context_object_name = 'liturgicalmanuscripts'


@login_required(login_url='/login/')
def edit_liturgicalmanuscript(request, pk=None, focus='', view='complete'):
    names = 'liturgicalmanuscriptsaint_formset,liturgicalmanuscriptchurch_formset'
    return edit_model(request, __name__, 'LiturgicalManuscript', 'saints', pk, formset_names=names,
                      focus=focus, view=view)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class LiturgicalManuscriptUpdateView(UpdateView):
    model = LiturgicalManuscript
    fields = '__all__'
    success_url = reverse_lazy('saints:liturgicalmanuscript-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class LiturgicalManuscriptDeleteView(DeleteView):
    model = LiturgicalManuscript
    success_url = reverse_lazy("saints:liturgicalmanuscript-list")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class LiturgicalManuscriptDetailView(DetailView):
    model = LiturgicalManuscript


# Rite
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RiteListView(ListView):
    model = Rite
    template_name = 'installations/rite_list.html'
    context_object_name = 'rites'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RiteCreatView(CreateView):
    model = Rite
    fields = '__all__'
    template_name = 'saints/rite_form.html'
    success_url = reverse_lazy('saints:rite-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RiteUpdateView(UpdateView):
    model = Rite
    fields = '__all__'
    success_url = reverse_lazy('saints:rite-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RiteDeleteView(DeleteView):
    model = Rite
    success_url = reverse_lazy("saints:rite-list")


# ManuscriptType
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ManuscriptTypeListView(ListView):
    model = ManuscriptType
    template_name = 'installations/manuscripttype_list.html'
    context_object_name = 'manuscripttypes'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ManuscriptTypeCreatView(CreateView):
    model = ManuscriptType
    fields = '__all__'
    template_name = 'saints/manuscripttype_form.html'
    success_url = reverse_lazy('saints:manuscripttype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ManuscriptTypeUpdateView(UpdateView):
    model = ManuscriptType
    fields = '__all__'
    success_url = reverse_lazy('saints:manuscripttype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ManuscriptTypeDeleteView(DeleteView):
    model = ManuscriptType
    success_url = reverse_lazy("saints:manuscripttype-list")


# ObjectType
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ObjectTypeListView(ListView):
    model = ObjectType
    template_name = 'installations/objecttype_list.html'
    context_object_name = 'objecttypes'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ObjectTypeCreatView(CreateView):
    model = ObjectType
    fields = '__all__'
    template_name = 'saints/objecttype_form.html'
    success_url = reverse_lazy('saints:objecttype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ObjectTypeUpdateView(UpdateView):
    model = ObjectType
    fields = '__all__'
    success_url = reverse_lazy('saints:objecttype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ObjectTypeDeleteView(DeleteView):
    model = ObjectType
    success_url = reverse_lazy("saints:objecttype-list")


# SaintType
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SaintTypeListView(ListView):
    model = SaintType
    template_name = 'installations/sainttype_list.html'
    context_object_name = 'sainttypes'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SaintTypeCreatView(CreateView):
    model = SaintType
    fields = '__all__'
    template_name = 'saints/sainttype_form.html'
    success_url = reverse_lazy('saints:sainttype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SaintTypeUpdateView(UpdateView):
    model = SaintType
    fields = '__all__'
    success_url = reverse_lazy('saints:sainttype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SaintTypeDeleteView(DeleteView):
    model = SaintType
    success_url = reverse_lazy("saints:sainttype-list")


# InstitutionType
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InstitutionTypeListView(ListView):
    model = InstitutionType
    template_name = 'installations/institutiontype_list.html'
    context_object_name = 'institutiontypes'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InstitutionTypeCreatView(CreateView):
    model = InstitutionType
    fields = '__all__'
    template_name = 'saints/institutiontype_form.html'
    success_url = reverse_lazy('saints:institutiontype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InstitutionTypeUpdateView(UpdateView):
    model = InstitutionType
    fields = '__all__'
    success_url = reverse_lazy('saints:institutiontype-list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InstitutionTypeDeleteView(DeleteView):
    model = InstitutionType
    success_url = reverse_lazy("saints:institutiontype-list")
