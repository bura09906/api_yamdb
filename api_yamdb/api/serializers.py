from django.forms import ValidationError
from rest_framework import serializers
from reviews.models import Comment, Review
from rest_framework import serializers
from rest_framework import serializers
from users.models import ConfirmationCode


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


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


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для представления регистрации пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        confrimation_code = validated_data.pop('confirmation_code')
        user = User.objects.create(**validated_data)
        ConfirmationCode.objects.create(user=user, code=confrimation_code)
        return user

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать "me" в качестве username'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена"""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с профилем пользователя"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
