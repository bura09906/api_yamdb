from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Comment, Review, User
from titles.models import Category, Genre, Title
from .filters import TitleFilter
from .permissions import (IsAuthorOrAdminOrRead, IsAdmin,
                          IsAuthenticatedAdminOrRead)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class CategoryViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedAdminOrRead,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedAdminOrRead,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects
                .annotate(rating=Avg("reviews__score")).all()
                .order_by("name")
                )
    permission_classes = (IsAuthenticatedAdminOrRead,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrRead,)
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
    permission_classes = (IsAuthorOrAdminOrRead,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class RegistationApiView(views.APIView):
    """Представление для регистрации пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_confirmation_code(self, user):
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код для получения токена',
            f'Ваш проверочный код: {confirmation_code}',
            settings.EMAIL_HOST_USER,
            [user.email]
        )


class GetTokenApiView(views.APIView):
    """Представление для получения токена"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_registered_user()
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)}, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Представление для работы с профилем пользователя.
    Права доступа админа и суперпользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
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
        elif request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.fields['role'].read_only = True
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
