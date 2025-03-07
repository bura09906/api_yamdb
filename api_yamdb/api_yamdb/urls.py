from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

API_VERSION = 'v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{API_VERSION}/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
