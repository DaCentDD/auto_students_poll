from django.conf import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('accounts.urls')),
    path('', include('polls.urls'))
]
