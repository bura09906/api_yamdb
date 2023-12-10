from rest_framework import routers
from django.urls import include, path
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

from .views import (CommentViewSet, GetTokenApiView, RegistationApiView,
                    ReviewViewSet, UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'comments', CommentViewSet, basename='comments')
router_v1.register(r'reviews', ReviewViewSet, basename='reviews')
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('auth/signup/', RegistationApiView.as_view()),
    path('auth/token/', GetTokenApiView.as_view()),
    path('', include(router_v1.urls)),
    path('/titles/<int:title_id>/', include(router_v1.urls)),
    path('/titles/<int:title_id>/reviews/', include(router_v1.urls)),
    path('/titles/<int:title_id>/reviews/<int:review_id>/',
         include(router_v1.urls)),
    path('/titles/<int:title_id>/reviews/<int:review_id>/comments/',
         include(router_v1.urls)),
]
