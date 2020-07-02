from django.conf.urls import url
from django.urls import path
from . import views

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
]