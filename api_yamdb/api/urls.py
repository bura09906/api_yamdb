from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenApiView, RegistationApiView, ReviewViewSet,
                    TitleViewSet, UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('comments', CommentViewSet, basename='comments')
router_v1.register('reviews', ReviewViewSet, basename='reviews')
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)

urlpatterns = [
    path('auth/signup/', RegistationApiView.as_view()),
    path('auth/token/', GetTokenApiView.as_view()),
    path('', include(router_v1.urls)),
    path('titles/<int:title_id>/', include(router_v1.urls)),
    path('titles/<int:title_id>/reviews/', include(router_v1.urls)),
    path('titles/<int:title_id>/reviews/<int:review_id>/',
         include(router_v1.urls)),
    path('titles/<int:title_id>/reviews/<int:review_id>/comments/',
         include(router_v1.urls)),
]
