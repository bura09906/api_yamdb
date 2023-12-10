from rest_framework import routers
from django.urls import include, path
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router_v1.urls))
]