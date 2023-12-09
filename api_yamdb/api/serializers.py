from django.forms import ValidationError
from rest_framework import serializers
from reviews.models import Comment, Review
from rest_framework import serializers


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
