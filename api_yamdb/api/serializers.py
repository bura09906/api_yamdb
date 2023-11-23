from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail

from reviews.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для представления регистрации пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email')

    def send_massege(self, validated_data):
        send_mail(
            'Тест', 'Тестовое сообщение',
            settings.EMAIL_HOST_USER,
            [validated_data.get('email')]
        )
