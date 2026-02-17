"""
Сериализаторы для REST API
"""
from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзывов через API
    """
    class Meta:
        model = Feedback
        fields = [
            'id', 'client_name', 'client_phone', 'client_email',
            'rating', 'category', 'text', 'source', 'telegram_user_id',
            'sentiment', 'created_at', 'is_processed'
        ]
        read_only_fields = ['id', 'sentiment', 'created_at', 'is_processed']
    
    def validate_rating(self, value):
        """Валидация оценки"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5")
        return value


class FeedbackStatsSerializer(serializers.Serializer):
    """
    Сериализатор для статистики отзывов
    """
    total_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    positive_count = serializers.IntegerField()
    neutral_count = serializers.IntegerField()
    negative_count = serializers.IntegerField()
    by_category = serializers.DictField()
    by_source = serializers.DictField()
