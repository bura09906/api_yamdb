from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet, ReviewViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import GetTokenApiView, RegistationApiView, UserViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('/titles/<int:title_id>/', include(router.urls)),
    path('/titles/<int:title_id>/reviews/', include(router.urls)),
    path('/titles/<int:title_id>/reviews/<int:review_id>/',
         include(router.urls)),
    path('/titles/<int:title_id>/reviews/<int:review_id>/comments/',
         include(router.urls)),

from .views import GetTokenApiView, RegistationApiView, UserViewSet


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path(f'auth/signup/', RegistationApiView.as_view()),
    path(f'auth/token/', GetTokenApiView.as_view()),
    path(f'', include(router_v1.urls))
]
