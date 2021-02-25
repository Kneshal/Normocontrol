from django.urls import path

from . import views

app_name = 'verify'

urlpatterns = [
    path('', views.index, name='index'),
    path('converter', views.converter, name='converter'),
    path('checks/archive/', views.archive, name='archive'),
    path('checks/new_check/', views.new_check, name='new_check'),
    path('group/new_group/', views.new_group, name='new_group'),
    path('checks/<int:check_id>/view',
         views.check_view,
         name='check_view'),
    path('checks/<int:check_id>/delete',
         views.check_delete,
         name='check_delete'),
    path('checks/<int:check_id>/archive',
         views.check_archive,
         name='check_archive'),
]
