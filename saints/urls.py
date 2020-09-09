from django.conf.urls import url
from django.urls import path
from . import views

# TEMPLATE URLS
app_name = 'saints'

urlpatterns = [
    path('', views.home, name='home'), # get and post req. for insert operation
    path('church/new/', views.churchCreate, name='church-insert'), # get and post req. for insert operation
    path('church/new/<int:id>/', views.churchCreate, name='church-update'), # get and post req. for update operation
    path('church/delete/<int:id>/', views.churchDelete, name='church-delete'),
    path('church/list/', views.churchList, name='church-list'),  # get request to retrieve and display all records
    path('bibliography/new/', views.bibliographyCreate, name='bibliography-insert'), # get and post req. for insert operation
    path('bibliography/new/<int:id>/', views.bibliographyCreate, name='bibliography-update'), # get and post req. for update operation
    path('bibliography/delete/<int:id>/', views.bibliographyDelete, name='bibliography-delete'),
    path('bibliography/list/', views.bibliographyList, name='bibliography-list'),  # get request to retrieve and display all records
    url(r'^inscription/new/$', views.InscriptionCreatView.as_view(), name='inscription-insert'),
    url(r'^inscription/new/(?P<pk>\d+)/$', views.InscriptionUpdateView.as_view(), name='inscription-update'),
    url(r'^inscription/delete/(?P<pk>\d+)/$', views.InscriptionDeleteView.as_view(), name='inscription-delete'),
    path('inscription/list', views.InscriptionListView.as_view(), name='inscription-list'),
    url(r'^saint/new/$', views.SaintCreatView.as_view(), name='saint-insert'),
    url(r'^saint/new/(?P<pk>\d+)/$', views.SaintUpdateView.as_view(), name='saint-update'),
    url(r'^saint/delete/(?P<pk>\d+)/$', views.SaintDeleteView.as_view(), name='saint-delete'),
    path('saint/list', views.SaintListView.as_view(), name='saint-list'),
    url(r'^object/new/$', views.ObjectCreatView.as_view(), name='object-insert'),
    url(r'^object/new/(?P<pk>\d+)/$', views.ObjectUpdateView.as_view(), name='object-update'),
    url(r'^object/delete/(?P<pk>\d+)/$', views.ObjectDeleteView.as_view(), name='object-delete'),
    path('object/list', views.ObjectListView.as_view(), name='object-list'),
    url(r'^feast/new/$', views.FeastCreatView.as_view(), name='feast-insert'),
    url(r'^feast/new/(?P<pk>\d+)/$', views.FeastUpdateView.as_view(), name='feast-update'),
    url(r'^feast/delete/(?P<pk>\d+)/$', views.FeastDeleteView.as_view(), name='feast-delete'),
    path('feast/list', views.FeastListView.as_view(), name='feast-list'),
    url(r'^liturgicalmanuscript/new/$', views.LiturgicalManuscriptCreatView.as_view(), name='liturgicalmanuscript-insert'),
    url(r'^liturgicalmanuscript/new/(?P<pk>\d+)/$', views.LiturgicalManuscriptUpdateView.as_view(), name='liturgicalmanuscript-update'),
    url(r'^liturgicalmanuscript/delete/(?P<pk>\d+)/$', views.LiturgicalManuscriptDeleteView.as_view(), name='liturgicalmanuscript-delete'),
    path('liturgicalmanuscript/list', views.LiturgicalManuscriptListView.as_view(), name='liturgicalmanuscript-list'),
    url(r'^rite/new/$', views.RiteCreatView.as_view(), name='rite-insert'),
    url(r'^rite/new/(?P<pk>\d+)/$', views.RiteUpdateView.as_view(), name='rite-update'),
    url(r'^rite/delete/(?P<pk>\d+)/$', views.RiteDeleteView.as_view(), name='rite-delete'),
    path('rite/list', views.RiteListView.as_view(), name='rite-list'),
]