"""
URL конфигурация для приложения feedback
"""
from django.urls import path
from . import views

urlpatterns = [
    # Публичные страницы
    path('', views.FeedbackSubmitView.as_view(), name='feedback_submit'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Страницы для авторизованных пользователей
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('feedbacks/', views.FeedbackListView.as_view(), name='feedback_list'),
    path('feedbacks/<int:pk>/', views.feedback_detail_view, name='feedback_detail'),
    
    # API endpoints
    path('api/feedback/submit/', views.api_feedback_submit, name='api_feedback_submit'),
    path('api/feedback/stats/', views.api_feedback_stats, name='api_feedback_stats'),
]
