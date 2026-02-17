"""
Management команда для создания тестовых пользователей
"""
from django.core.management.base import BaseCommand
from feedback.models import User


class Command(BaseCommand):
    help = 'Создание тестовых пользователей (администратор и менеджер)'

    def handle(self, *args, **options):
        """
        Создает тестовых пользователей для системы
        """
        # Создание администратора
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role=User.Role.ADMINISTRATOR,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Создан администратор: username=admin, password=admin123'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Администратор уже существует')
            )
        
        # Создание менеджера
        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user(
                username='manager',
                email='manager@example.com',
                password='manager123',
                role=User.Role.MANAGER
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Создан менеджер: username=manager, password=manager123'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Менеджер уже существует')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Тестовые пользователи готовы к использованию!')
        )
