from django.urls import path

from . import views

app_name = 'verify'

urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('students/',
         views.student_list,
         name='student_list'),
    path('group/',
         views.group_list,
         name='group_list'),
    path('group/new_group/',
         views.new_group,
         name='new_group'),
    path('group/<slug:slug>/',
         views.group_students,
         name='group_students'),
    path('user/<str:username>/check_list',
         views.check_list,
         name='check_list'),
    path('user/<str:username>/archive/',
         views.archive,
         name='archive'),
    path('user/<str:username>/new_check/',
         views.new_check,
         name='new_check'),
    path('user/<str:username>/<int:check_id>/new_remark/',
         views.new_remark,
         name='new_remark'),
    path('user/<str:username>/<int:check_id>/check_view',
         views.check_view,
         name='check_view'),
    path('user/<str:username>/<int:check_id>/check_delete',
         views.check_delete,
         name='check_delete'),
    path('user/<str:username>/<int:check_id>/check_archive',
         views.check_archive,
         name='check_archive'),
]
