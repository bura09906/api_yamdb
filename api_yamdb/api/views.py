from rest_framework import viewsets
from reviews.models import Comment, Title, User, Review, Genre, Category, Title
from api.serializers import (
    CommentSerializer, ReviewSerializer, GenreSerializer,
    CategorySerializer
)
from django.shortcuts import get_object_or_404
import secrets

from django.db.models import Avg
from users.models import ConfirmationCode
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import ForAdminOrSurepUser, IsAuthorOrReadOnly
from .serializers import (GetTokenSerializer, ProfileSerializer,
                          RegistrationSerializer, UserSerializer)


from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .serializers import GenreSerializer, CategorySerializer, TitleWriteSerializer, TitleReadSerializer
from reviews.models import Title, Genre, Category


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
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = ProfileSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(
            _average_rating=Avg('rating__score')
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
