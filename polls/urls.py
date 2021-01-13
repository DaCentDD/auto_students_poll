from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.main, name='main'),
    path('student_page/', views.main, name='student_page'),
    path('student_page/<pk>', views.student_page, name='student_page'),
    path('student_page/<pk>/poll/<id>', views.poll_enter, name='poll_enter'),
    path('student_page/<pk>/poll/<id>/finish', views.poll_finish, name='poll_finish'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('groups/', views.groups_menu, name='group_menu'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/group/<pk>', views.group, name='group'),
    path('groups/group/<pk>/delete', views.group_delete, name='group_delete'), 
    path('students/create/', views.student_create, name='student_create'),
    path('students/', views.students_menu, name='student_menu'),
    path('students/student/<pk>', views.student, name='student'),
    path('students/student/<pk>/delete', views.student_delete, name='student_delete'),
    path('students/student/<pk>/password', views.student_password, name='students_password'),
    path('polls/', views.polls_menu, name='polls_menu'),
    path('polls/create/', views.poll_create, name='poll_create'),
    path('polls/poll/<pk>', views.poll, name='poll'),
    path('polls/poll/<pk>/delete', views.poll_delete, name='poll_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)