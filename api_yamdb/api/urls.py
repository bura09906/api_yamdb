from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet, ReviewViewSet, GenreViewSet, CategoryViewSet, TitleViewSet
)
from .views import GetTokenApiView, RegistationApiView, UserViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitleViewSet, basename='titles')
API_VERSION = 'v1'

#Изменил v1
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/titles/<int:title_id>/', include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/', include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/',
         include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/comments/',
         include(router.urls)),
         
    path(f'{API_VERSION}/auth/signup/', RegistationApiView.as_view()),
    path(f'{API_VERSION}/auth/token/', GetTokenApiView.as_view()),
    path(f'{API_VERSION}/', include(router.urls))
]
