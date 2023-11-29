from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenApiView, RegistationApiView, UserViewSet

API_VERSION = 'v1'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path(f'{API_VERSION}/auth/signup/', RegistationApiView.as_view()),
    path(f'{API_VERSION}/auth/token/', GetTokenApiView.as_view()),
    path(f'{API_VERSION}/', include(router_v1.urls))
]
