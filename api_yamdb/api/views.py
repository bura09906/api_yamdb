import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import ConfirmationCode

from .permissions import ForAdminOrSurepUser
from .serializers import (GetTokenSerializer, ProfileSerializer,
                          RegistrationSerializer, UserSerializer)


class RegistationApiView(views.APIView):
    """Представление для регистрации пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        confirmation_code = secrets.token_urlsafe(
            settings.LENGTH_CONFIRMATION_CODE
        )
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
            ConfirmationCode.objects.filter(
                user=user
            ).update(code=confirmation_code)
            self.send_confirmation_code(confirmation_code, request.data)
            return Response(request.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data[
                    'confirmation_code'
                ] = confirmation_code
                self.send_confirmation_code(
                    confirmation_code, serializer.validated_data
                )
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def send_confirmation_code(self, code, data):
        email = data.get('email')
        send_mail(
            'Код для получения токена',
            f'Ваш проверочный код: {code}',
            settings.EMAIL_HOST_USER,
            [email]
        )


class GetTokenApiView(views.APIView):
    """Представление для получения токена"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            user = get_object_or_404(User, username=username)
            if user.confirmationcode.code != confirmation_code:
                return Response(
                    {'error': 'недействительный проверочный код'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Представление для работы с профилем пользователя.
    Права доступа админа и суперпользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [ForAdminOrSurepUser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)
    ordering = ('id',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = ProfileSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
