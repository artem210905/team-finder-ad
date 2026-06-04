from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('projects:project_list', permanent=False)),
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
]
