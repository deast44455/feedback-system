"""
Настройка Django Admin для системы отзывов
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Feedback


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Админка для кастомной модели пользователя
    """
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительные настройки', {'fields': ('role',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительные настройки', {'fields': ('role',)}),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Админка для отзывов
    """
    list_display = [
        'client_name', 'rating', 'category', 'sentiment', 
        'source', 'is_processed', 'created_at'
    ]
    list_filter = [
        'source', 'category', 'sentiment', 'rating', 
        'is_processed', 'created_at'
    ]
    search_fields = [
        'client_name', 'client_email', 'client_phone', 
        'text', 'response'
    ]
    readonly_fields = ['created_at', 'updated_at', 'sentiment']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('client_name', 'client_email', 'client_phone', 'telegram_user_id')
        }),
        ('Детали отзыва', {
            'fields': ('source', 'rating', 'category', 'text', 'sentiment')
        }),
        ('Обработка', {
            'fields': ('is_processed', 'processed_by', 'response')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Делаем некоторые поля readonly при редактировании"""
        if obj:  # Если объект существует (редактирование)
            return self.readonly_fields + ['source', 'created_at', 'updated_at']
        return self.readonly_fields
