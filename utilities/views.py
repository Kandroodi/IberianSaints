from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from utils import view_util
from utils.view_util import Crud, Cruds, make_tabs, FormsetFactoryManager
from .models import copy_complete
from utilities.search import Search
from django.db.models import Q
from django.db.models.functions import Lower




def list_view(request, model_name, app_name):
    '''list view of a model.'''
    s = Search(request, model_name, app_name)
    instances = s.filter()
    if model_name == 'UserLoc': model_name = 'location'
    var = {model_name.lower() + '_list': instances, 'page_name': model_name,
           'order': s.order.order_by, 'direction': s.order.direction,
           'query': s.query.query, 'nentries': s.nentries}
    print(s.notes, 000)
    return render(request, app_name + '/' + model_name.lower() + '_list.html', var)


# @permission_required('utilities.add_generic')
def edit_model(request, name_space, model_name, app_name, instance_id=None,
               formset_names='', focus='', view='complete'):
    '''edit view generalized over models.
    assumes a 'add_{{model_name}}.html template and edit_{{model_name}} function
    and {{model_name}}Form
    '''
    names = formset_names
    model = apps.get_model(app_name, model_name)
    modelform = view_util.get_modelform(name_space, model_name + 'Form')
    instance = model.objects.get(pk=instance_id) if instance_id else None
    crud = Crud(instance) if instance else None
    ffm, form = None, None
    if request.method == 'POST':
        focus, button = getfocus(request), getbutton(request)
        if button in 'delete,cancel,confirm_delete':
            return delete_model(request, name_space, model_name, app_name, instance_id)
        if button == 'saveas' and instance: instance = copy_complete(instance)
        form = modelform(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            print('form is valid: ', form.cleaned_data, type(form))

            instance = form.save()
            if view == 'complete':
                ffm = FormsetFactoryManager(name_space, names, request, instance)
                valid = ffm.save()
                if valid:
                    show_messages(request, button, model_name)
                    if button == 'add_another':
                        # return HttpResponseRedirect(reverse(app_name + ':add_' + model_name.lower()))
                        return HttpResponseRedirect(reverse(app_name + ':' + model_name.lower() + '-insert'))
                    # return HttpResponseRedirect(reverse(
                    #     app_name + ':edit_' + model_name.lower(),
                    #     kwargs={'pk': instance.pk, 'focus': focus}))
                    return HttpResponseRedirect(reverse(
                        app_name + ':' + model_name.lower() + '-update',
                        kwargs={'pk': instance.pk, 'focus': focus}))
                else:
                    print('ERROR', ffm.errors)
            else:
                return HttpResponseRedirect('/utilities/close/')
    if not form: form = modelform(instance=instance)
    if not ffm: ffm = FormsetFactoryManager(name_space, names, instance=instance)
    tabs = make_tabs(model_name.lower(), focus_names=focus)
    page_name = 'Edit ' + model_name.lower() if instance_id else 'Add ' + model_name.lower()
    args = {'form': form, 'page_name': page_name, 'crud': crud,
            'tabs': tabs, 'view': view}
    args.update(ffm.dict)
    return render(request, app_name + '/add_' + model_name.lower() + '.html', args)


# @permission_required('utilities.add_generic')
def add_simple_model(request, name_space, model_name, app_name, page_name):
    '''Function to add simple models with only a form could be extended.
    request 	django object
    name_space 	the name space of the module calling this function (to load forms / models)
    model_name 	name of the model
    app_name 	name of the app
    page_name 	name of the page
    The form name should be of format <model_name>Form
    '''
    modelform = view_util.get_modelform(name_space, model_name + 'Form')
    form = modelform(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, model_name + ' saved')
            return HttpResponseRedirect('/utilities/close/')
    model = apps.get_model(app_name, model_name)
    instances = model.objects.all().order_by('name')
    var = {'form': form, 'page_name': page_name, 'instances': instances}
    return render(request, 'utilities/add_simple_model.html', var)


# @permission_required('utilities.delete_generic')
def delete_model(request, name_space, model_name, app_name, pk):
    model = apps.get_model(app_name, model_name)
    instance = get_object_or_404(model, id=pk)
    focus, button = getfocus(request), getbutton(request)
    print(request.POST.keys())
    print(99, instance.view(), instance, 888)
    print(button)
    if request.method == 'POST':
        if button == 'cancel':
            show_messages(request, button, model_name)
            # return HttpResponseRedirect(reverse(
            #     app_name + ':edit_' + model_name.lower(),
            #     kwargs={'pk': instance.pk, 'focus': focus}))
            return HttpResponseRedirect(reverse(
                app_name + ':' + model_name.lower() + '-update',
                kwargs={'pk': instance.pk, 'focus': focus}))
        if button == 'confirm_delete':
            instance.delete()
            show_messages(request, button, model_name)
            return HttpResponseRedirect('/' + app_name + '/' + model_name.lower())
    info = instance.info
    print(1, info, instance, pk)
    var = {'info': info, 'page_name': 'Delete ' + model_name.lower()}
    print(2)
    return render(request, 'utilities/delete_model.html', var)


def getfocus(request):
    '''extracts focus variable from the request object to correctly set the active tabs.'''
    if 'focus' in request.POST.keys():
        return request.POST['focus']
    else:
        return 'default'


# Create your views here.
def getbutton(request):
    if 'save' in request.POST.keys():
        return request.POST['save']
    else:
        return 'default'


def show_messages(request, button, model_name):
    '''provide user feedback on submitting a form.'''
    if button == 'saveas':
        messages.warning(request,
                         'saved a copy of ' + model_name + '. Use "save" button to store edits to this copy')
    elif button == 'confirm_delete':
        messages.success(request, model_name + ' deleted')
    elif button == 'cancel':
        messages.warning(request, 'delete aborted')
    else:
        messages.success(request, model_name + ' saved')


def close(request):
    '''page that closes itself for on the fly creation of model instances (loaded in a new tab).'''
    return render(request, 'utilities/close.html')


# Search functions
# -----------------------------------------------------------------------------------------------------------------------
def saintsimplesearch(request, app_name, model_name):
    '''Search function between all fields in a model.
    app_name : saints
    model_name : saint
    '''
    model = apps.get_model(app_name, model_name)
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = model.objects.all().order_by(order_by)
    # -----------------------------------------------------------
    queries = query.split()
    if query is not None:
        query_setall = model.objects.none()
        for qs in queries:
            query_seti = query_set.filter(
                Q(name__icontains=qs) |
                Q(feast_day__icontains=qs) |
                Q(death_date__icontains=qs) |
                Q(death_place__icontains=qs) |
                Q(type__name__icontains=qs) |
                Q(external_link__icontains=qs) |
                Q(description__icontains=qs)
            )
            query_setall = query_setall | query_seti
        query_set = query_setall.order_by(order_by)
    if query == "":
        query_set = model.objects.all().order_by(order_by)

    return query_set.distinct()


def churchsimplesearch(request, app_name, model_name):
    '''Search function between all fields in a model.
    app_name : saints
    model_name : church
    '''
    model = apps.get_model(app_name, model_name)
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = model.objects.all().order_by(order_by)
    # -----------------------------------------------------------
    queries = query.split()
    if query is not None:
        query_setall = model.objects.none()
        for qs in queries:
            query_seti = query_set.filter(
                Q(name__icontains=qs) |
                Q(date_lower__icontains=qs) |
                Q(date_upper__icontains=qs) |
                Q(institution_type__name__icontains=qs) |
                Q(bibliography_many__short_title__icontains=qs) |
                Q(external_link__icontains=qs) |
                Q(description__icontains=qs)
            )
            query_setall = query_setall | query_seti
        query_set = query_setall.order_by(order_by)
    if query == "":
        query_set = model.objects.all().order_by(order_by)

    return query_set.distinct()


def objectsimplesearch(request, app_name, model_name):
    '''Search function between all fields in a model.
    app_name : saints
    model_name : object
    '''
    model = apps.get_model(app_name, model_name)
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = model.objects.all().order_by(order_by)
    # -----------------------------------------------------------
    queries = query.split()
    if query is not None:
        query_setall = model.objects.none()
        for qs in queries:
            query_seti = query_set.filter(
                Q(name__icontains=qs) |
                Q(date_lower__icontains=qs) |
                Q(date_upper__icontains=qs) |
                Q(original_location__name__icontains=qs) |
                Q(current_location__name__icontains=qs) |
                Q(type__name__icontains=qs) |
                Q(bibliography_many__short_title__icontains=qs) |
                Q(external_link__icontains=qs) |
                Q(description__icontains=qs)
            )
            query_setall = query_setall | query_seti
        query_set = query_setall.order_by(order_by)
    if query == "":
        query_set = model.objects.all().order_by(order_by)

    return query_set.distinct()


def inscriptionsimplesearch(request, app_name, model_name):
    '''Search function between all fields in a model.
    app_name : saints
    model_name : inscription
    '''
    model = apps.get_model(app_name, model_name)
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = model.objects.all().order_by(order_by)
    # -----------------------------------------------------------
    queries = query.split()
    if query is not None:
        query_setall = model.objects.none()
        for qs in queries:
            query_seti = query_set.filter(
                Q(reference_no__icontains=qs) |
                Q(date_lower__icontains=qs) |
                Q(date_upper__icontains=qs) |
                Q(original_location__name__icontains=qs) |
                Q(text__icontains=qs) |
                Q(bibliography_many__short_title__icontains=qs) |
                Q(external_link__icontains=qs) |
                Q(description__icontains=qs)
            )
            query_setall = query_setall | query_seti
        query_set = query_setall.order_by(order_by)
    if query == "":
        query_set = model.objects.all().order_by(order_by)

    return query_set.distinct()



def liturgicalmanuscriptsimplesearch(request, app_name, model_name):
    '''Search function between all fields in a model.
    app_name : saints
    model_name : liturgicalmanuscript
    '''
    model = apps.get_model(app_name, model_name)
    query = request.GET.get("q", "")
    order_by = request.GET.get("order_by", "id")
    query_set = model.objects.all().order_by(order_by)
    # -----------------------------------------------------------
    queries = query.split()
    if query is not None:
        query_setall = model.objects.none()
        for qs in queries:
            query_seti = query_set.filter(
                Q(shelf_no__icontains=qs) |
                Q(rite__name__icontains=qs) |
                Q(type__name__icontains=qs) |
                Q(provenance__name__icontains=qs) |
                Q(date_lower__icontains=qs) |
                Q(date_upper__icontains=qs) |
                Q(bibliography_many__short_title__icontains=qs) |
                Q(external_link__icontains=qs) |
                Q(description__icontains=qs)
            )
            query_setall = query_setall | query_seti
        query_set = query_setall.order_by(order_by)
    if query == "":
        query_set = model.objects.all().order_by(order_by)

    return query_set.distinct()