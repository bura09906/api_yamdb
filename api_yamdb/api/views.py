from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin

from reviews.models import User
from .serializers import RegistrationSerializer
from rest_framework import permissions


class RegictsrationViewset(
    CreateModelMixin, viewsets.GenericViewSet
):
    """Представление для регистрации пользователя"""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
