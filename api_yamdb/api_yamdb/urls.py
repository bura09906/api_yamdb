from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import include, path
>>>>>>> 06fa757d5ac21d97808d4410f450044f38d1e127
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
