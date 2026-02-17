"""
Система прав доступа и аутентификация для API
"""
from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class APIKeyAuthentication(BaseAuthentication):
    """
    Аутентификация по API ключу для Telegram бота
    """
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None
        
        if api_key != settings.API_KEY:
            raise AuthenticationFailed('Неверный API ключ')
        
        # Возвращаем None в качестве пользователя, так как это API для бота
        return (None, None)


class IsManagerOrAdmin(permissions.BasePermission):
    """
    Разрешение только для менеджеров и администраторов
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role in ['MANAGER', 'ADMINISTRATOR']


class IsAdministrator(permissions.BasePermission):
    """
    Разрешение только для администраторов
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role == 'ADMINISTRATOR'
