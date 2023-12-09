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
]
