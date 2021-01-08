from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.main, name='main'),
    path('student_page/', views.student_page, name='student_page'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('poll/create/', views.poll_create, name='poll_create'),
    path('groups/', views.groups_menu, name='group_menu'),
    path('groups/<pk>', views.group, name='group'),
    path('group_create/', views.group_create, name='group_create'),
    path('student_create/', views.student_create, name='student_create'),
    path('students/', views.students_menu, name='student_menu'),
    path('students/<pk>', views.student, name='students'),
    path('students/<pk>/delete', views.student_delete, name='student_delete'),
    path('students/<pk>/password', views.student_password, name='students_password'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)