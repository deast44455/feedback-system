"""
Views для системы сбора и анализа отзывов
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Feedback, User
from .forms import FeedbackForm, FeedbackResponseForm
from .serializers import FeedbackSerializer, FeedbackStatsSerializer
from .permissions import APIKeyAuthentication, IsManagerOrAdmin


class FeedbackSubmitView(CreateView):
    """
    Публичная страница для отправки отзывов
    """
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/submit.html'
    success_url = reverse_lazy('feedback_submit')
    
    def form_valid(self, form):
        """Обработка успешной отправки формы"""
        form.instance.source = 'WEB'
        messages.success(
            self.request,
            'Спасибо за ваш отзыв! Мы обязательно его рассмотрим.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Обработка ошибок валидации"""
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)


def login_view(request):
    """
    Страница авторизации
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'feedback/login.html')


@login_required
def logout_view(request):
    """
    Выход из системы
    """
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('feedback_submit')


class ManagerOrAdminMixin(UserPassesTestMixin):
    """
    Mixin для проверки прав доступа (только менеджеры и администраторы)
    """
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.role in ['MANAGER', 'ADMINISTRATOR']


@login_required
def dashboard_view(request):
    """
    Дашборд со статистикой и графиками
    """
    # Проверка прав доступа
    if request.user.role not in ['MANAGER', 'ADMINISTRATOR']:
        messages.error(request, 'У вас нет доступа к этой странице')
        return redirect('feedback_submit')
    
    # Получение параметров фильтрации
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    category = request.GET.get('category')
    sentiment = request.GET.get('sentiment')
    source = request.GET.get('source')
    is_processed = request.GET.get('is_processed')
    
    # Базовый queryset
    feedbacks = Feedback.objects.all()
    
    # Применение фильтров
    if date_from:
        feedbacks = feedbacks.filter(created_at__gte=date_from)
    if date_to:
        feedbacks = feedbacks.filter(created_at__lte=date_to)
    if category:
        feedbacks = feedbacks.filter(category=category)
    if sentiment:
        feedbacks = feedbacks.filter(sentiment=sentiment)
    if source:
        feedbacks = feedbacks.filter(source=source)
    if is_processed == 'true':
        feedbacks = feedbacks.filter(is_processed=True)
    elif is_processed == 'false':
        feedbacks = feedbacks.filter(is_processed=False)
    
    # Общая статистика
    total_count = feedbacks.count()
    average_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Распределение по тональности
    sentiment_stats = feedbacks.values('sentiment').annotate(count=Count('id'))
    positive_count = next((s['count'] for s in sentiment_stats if s['sentiment'] == 'POSITIVE'), 0)
    neutral_count = next((s['count'] for s in sentiment_stats if s['sentiment'] == 'NEUTRAL'), 0)
    negative_count = next((s['count'] for s in sentiment_stats if s['sentiment'] == 'NEGATIVE'), 0)
    
    # Распределение по категориям
    category_stats = feedbacks.values('category').annotate(count=Count('id'))
    
    # Распределение по источникам
    source_stats = feedbacks.values('source').annotate(count=Count('id'))
    
    # Распределение оценок
    rating_stats = feedbacks.values('rating').annotate(count=Count('id')).order_by('rating')
    
    # Динамика по датам (последние 30 дней)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    timeline_data = []
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        count = feedbacks.filter(
            created_at__date=date.date()
        ).count()
        timeline_data.append({
            'date': date.strftime('%d.%m'),
            'count': count
        })
    
    context = {
        'total_count': total_count,
        'average_rating': round(average_rating, 2),
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'category_stats': list(category_stats),
        'source_stats': list(source_stats),
        'rating_stats': list(rating_stats),
        'timeline_data': timeline_data,
        'categories': Feedback.Category.choices,
        'sentiments': Feedback.Sentiment.choices,
        'sources': Feedback.Source.choices,
        'filters': {
            'date_from': date_from or '',
            'date_to': date_to or '',
            'category': category or '',
            'sentiment': sentiment or '',
            'source': source or '',
            'is_processed': is_processed or '',
        }
    }
    
    return render(request, 'feedback/dashboard.html', context)


class FeedbackListView(LoginRequiredMixin, ManagerOrAdminMixin, ListView):
    """
    Список всех отзывов
    """
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 20
    
    def get_queryset(self):
        """Получение отфильтрованного списка отзывов"""
        queryset = Feedback.objects.all()
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(client_name__icontains=search) |
                Q(text__icontains=search) |
                Q(client_email__icontains=search)
            )
        
        # Фильтры
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        sentiment = self.request.GET.get('sentiment')
        if sentiment:
            queryset = queryset.filter(sentiment=sentiment)
        
        source = self.request.GET.get('source')
        if source:
            queryset = queryset.filter(source=source)
        
        is_processed = self.request.GET.get('is_processed')
        if is_processed == 'true':
            queryset = queryset.filter(is_processed=True)
        elif is_processed == 'false':
            queryset = queryset.filter(is_processed=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Feedback.Category.choices
        context['sentiments'] = Feedback.Sentiment.choices
        context['sources'] = Feedback.Source.choices
        context['search'] = self.request.GET.get('search', '')
        context['filters'] = {
            'category': self.request.GET.get('category', ''),
            'sentiment': self.request.GET.get('sentiment', ''),
            'source': self.request.GET.get('source', ''),
            'is_processed': self.request.GET.get('is_processed', ''),
        }
        return context


@login_required
def feedback_detail_view(request, pk):
    """
    Детальный просмотр отзыва с возможностью ответа
    """
    # Проверка прав доступа
    if request.user.role not in ['MANAGER', 'ADMINISTRATOR']:
        messages.error(request, 'У вас нет доступа к этой странице')
        return redirect('feedback_submit')
    
    feedback = get_object_or_404(Feedback, pk=pk)
    
    if request.method == 'POST':
        form = FeedbackResponseForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            if feedback.is_processed and not feedback.processed_by:
                feedback.processed_by = request.user
            form.save()
            messages.success(request, 'Отзыв успешно обновлен')
            return redirect('feedback_detail', pk=pk)
    else:
        form = FeedbackResponseForm(instance=feedback)
    
    context = {
        'feedback': feedback,
        'form': form
    }
    
    return render(request, 'feedback/feedback_detail.html', context)


# API Views

@api_view(['POST'])
@authentication_classes([APIKeyAuthentication])
def api_feedback_submit(request):
    """
    API эндпоинт для приема отзывов от Telegram бота
    
    POST /api/feedback/submit/
    Headers: X-API-Key: your-api-key
    Body: {
        "client_name": "Иван Иванов",
        "client_phone": "+79001234567",
        "rating": 5,
        "category": "SERVICE",
        "text": "Отличное обслуживание!",
        "telegram_user_id": "123456789"
    }
    """
    serializer = FeedbackSerializer(data=request.data)
    
    if serializer.is_valid():
        # Устанавливаем источник как Telegram
        feedback = serializer.save(source='TELEGRAM')
        
        return Response({
            'success': True,
            'message': 'Отзыв успешно принят',
            'feedback_id': feedback.id
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Ошибка валидации данных',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([APIKeyAuthentication])
def api_feedback_stats(request):
    """
    API эндпоинт для получения статистики
    
    GET /api/feedback/stats/
    Headers: X-API-Key: your-api-key
    """
    feedbacks = Feedback.objects.all()
    
    total_count = feedbacks.count()
    average_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Распределение по тональности
    sentiment_stats = feedbacks.values('sentiment').annotate(count=Count('id'))
    positive_count = next((s['count'] for s in sentiment_stats if s['sentiment'] == 'POSITIVE'), 0)
    neutral_count = next((s['count'] for s in sentiment_stats if s['sentiment'] == 'NEUTRAL'), 0)
    negative_count = next((s['count'] for s in sentiment_stats if s['sentiment'] == 'NEGATIVE'), 0)
    
    # Распределение по категориям
    category_stats = {
        item['category']: item['count']
        for item in feedbacks.values('category').annotate(count=Count('id'))
    }
    
    # Распределение по источникам
    source_stats = {
        item['source']: item['count']
        for item in feedbacks.values('source').annotate(count=Count('id'))
    }
    
    stats_data = {
        'total_count': total_count,
        'average_rating': round(average_rating, 2),
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'by_category': category_stats,
        'by_source': source_stats
    }
    
    serializer = FeedbackStatsSerializer(stats_data)
    
    return Response({
        'success': True,
        'data': serializer.data
    })
