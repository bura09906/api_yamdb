from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenApiView, RegistationApiView, UserViewSet


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path(f'auth/signup/', RegistationApiView.as_view()),
    path(f'auth/token/', GetTokenApiView.as_view()),
    path(f'', include(router_v1.urls))
]
