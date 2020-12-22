from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'polls'

urlpatterns = [
    path('', views.main, name='main'),
    path('student_page/', views.student_page, name='student_page'),
    path('admin_page/', views.admin_page, name='admin_page')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)