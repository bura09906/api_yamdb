from django.forms import ValidationError
from rest_framework import serializers
from reviews.models import Comment, Review, User
from titles.models import Category, Genre, Title
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.db.models import Q

from users.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def to_representation(self, data):
        return TitleReadSerializer(
            context=self.context
        ).to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        title_id = self.context["view"].kwargs['title_id']
        user = self.context["request"].user
        if Review.objects.filter(title_id=title_id,
                                 author=user).exists():
            raise ValidationError(
                "Пользователь может оставить только один отзыв"
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор для представления регистрации пользователя"""
    username = serializers.CharField(max_length=150,
                                     validators=(
                                         [RegexValidator(regex=r"^[\w.@+-]+\Z")]
                                     ))
    email = serializers.EmailField(max_length=254)

    class Meta:
        fields = ('username', 'email')

    
    def validate(self, data):
        if User.objects.filter(Q(email=data['email']) | Q(username=data['username'])).exists():
            if User.objects.filter(email=data['email'], username=data['username']).exists():
                return data
            raise serializers.ValidationError(
                'Пользователь с указанным email или username уже существует'
            )
        return data

    def validate_username(self, value):
        if not validate_username(value):
            return value
    
    def create(self, validated_data):
        user, status = User.objects.get_or_create(username=validated_data['username'], email=validated_data['email'])
        return user


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена"""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user, data['confirmation_code']):
            raise serializers.ValidationError(
                'Недействительный проверочный код'
            )
        return data
    
    def get_registered_user(self):
        user = get_object_or_404(User, username=self.validated_data['username'])
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с профилем пользователя"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
