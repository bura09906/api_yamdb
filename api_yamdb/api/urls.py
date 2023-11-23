from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RegictsrationViewset

API_VERSION = 'v1'

router_v1 = DefaultRouter()
router_v1.register('auth/signup', RegictsrationViewset)

urlpatterns = [
    path(f'{API_VERSION}/', include(router_v1.urls)),
]
