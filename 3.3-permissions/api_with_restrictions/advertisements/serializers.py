from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, attrs):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context['request'].user
        posts = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if posts >= 10:
            raise serializers.ValidationError('Не более 10 открытых объявлений')
        return attrs

    def put(self, request, *args, **kwargs):
        user = self.context['request'].user
        posts = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if posts >= 10:
            return self.partial_update(request, *args, **kwargs)
