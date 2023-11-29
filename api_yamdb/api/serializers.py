from rest_framework import serializers
from reviews.models import User
from users.models import ConfirmationCode


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
