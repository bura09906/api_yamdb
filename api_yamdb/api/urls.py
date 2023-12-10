from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet, ReviewViewSet,
    GetTokenApiView, RegistationApiView, UserViewSet
)
from rest_framework import routers
from django.urls import include, path
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

API_VERSION = 'v1'

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'comments', CommentViewSet, basename='comments')
router_v1.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('API_VERSION', include(router_v1.urls)),
    path('API_VERSION/titles/<int:title_id>/reviews/', include(router_v1.urls)),
    path('API_VERSION/titles/<int:title_id>/reviews/<int:review_id>/comments/',
         include(router_v1.urls)),
    path(f'{API_VERSION}/auth/signup/', RegistationApiView.as_view()),
    path(f'{API_VERSION}/auth/token/', GetTokenApiView.as_view()),
    
]
