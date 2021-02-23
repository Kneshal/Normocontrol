from django.urls import path

from . import views

app_name = 'verify'

urlpatterns = [
    path('', views.index, name='index'),
    path('checks/new_check/', views.new_check, name='new_check'),
    path('group/new_group/', views.new_group, name='new_group'),
]
