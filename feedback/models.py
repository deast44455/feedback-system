"""
Модели данных для системы сбора отзывов
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Расширенная модель пользователя с системой ролей
    """
    class Role(models.TextChoices):
        ADMINISTRATOR = 'ADMINISTRATOR', 'Администратор'
        MANAGER = 'MANAGER', 'Менеджер'
        CLIENT = 'CLIENT', 'Клиент'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name='Роль'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Feedback(models.Model):
    """
    Модель отзыва от клиента
    """
    class Source(models.TextChoices):
        WEB = 'WEB', 'Веб-форма'
        TELEGRAM = 'TELEGRAM', 'Telegram'
    
    class Category(models.TextChoices):
        QUALITY = 'QUALITY', 'Качество продукта'
        SERVICE = 'SERVICE', 'Обслуживание'
        PRICE = 'PRICE', 'Цены'
        DELIVERY = 'DELIVERY', 'Доставка'
        OTHER = 'OTHER', 'Прочее'
    
    class Sentiment(models.TextChoices):
        POSITIVE = 'POSITIVE', 'Позитивный'
        NEUTRAL = 'NEUTRAL', 'Нейтральный'
        NEGATIVE = 'NEGATIVE', 'Негативный'
    
    # Информация о клиенте
    client_name = models.CharField(
        max_length=255,
        verbose_name='Имя клиента'
    )
    client_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email клиента'
    )
    client_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон клиента'
    )
    telegram_user_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Telegram User ID'
    )
    
    # Детали отзыва
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.WEB,
        verbose_name='Источник'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name='Категория'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    sentiment = models.CharField(
        max_length=20,
        choices=Sentiment.choices,
        default=Sentiment.NEUTRAL,
        verbose_name='Тональность'
    )
    
    # Метаданные
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    # Обработка отзыва
    is_processed = models.BooleanField(
        default=False,
        verbose_name='Обработан'
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_feedbacks',
        verbose_name='Обработан пользователем'
    )
    response = models.TextField(
        blank=True,
        null=True,
        verbose_name='Ответ на отзыв'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв от {self.client_name} - {self.rating}★ ({self.created_at.strftime('%d.%m.%Y')})"
    
    def save(self, *args, **kwargs):
        """
        При сохранении автоматически определяем тональность и категорию
        """
        # Импортируем здесь, чтобы избежать циклических импортов
        from .utils.sentiment_analysis import analyze_sentiment
        from .utils.category_detection import detect_category
        
        # Автоматическое определение тональности
        if not self.sentiment or self.sentiment == self.Sentiment.NEUTRAL:
            self.sentiment = analyze_sentiment(self.text, self.rating)
        
        # Автоматическое определение категории, если не указана или указана "Прочее"
        if not self.category or self.category == self.Category.OTHER:
            detected_category = detect_category(self.text)
            if detected_category:
                self.category = detected_category
        
        super().save(*args, **kwargs)
