<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/titles/<int:title_id>/', include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/', include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/',
         include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/comments/',
         include(router.urls)),
=======
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
>>>>>>> 06fa757d5ac21d97808d4410f450044f38d1e127
]
