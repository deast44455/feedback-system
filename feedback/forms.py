"""
Формы для работы с отзывами
"""
from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Форма для создания отзыва через веб-интерфейс
    """
    class Meta:
        model = Feedback
        fields = ['client_name', 'client_email', 'client_phone', 'rating', 'category', 'text']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя',
                'required': True
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.com (необязательно)'
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX (необязательно)'
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Расскажите о вашем опыте...',
                'required': True
            })
        }
        labels = {
            'client_name': 'Ваше имя',
            'client_email': 'Email (необязательно)',
            'client_phone': 'Телефон (необязательно)',
            'rating': 'Оценка',
            'category': 'Категория',
            'text': 'Текст отзыва'
        }
        help_texts = {
            'rating': 'Выберите оценку от 1 до 5 звезд',
            'category': 'Выберите наиболее подходящую категорию',
        }


class FeedbackResponseForm(forms.ModelForm):
    """
    Форма для ответа на отзыв (для менеджеров и администраторов)
    """
    class Meta:
        model = Feedback
        fields = ['response', 'is_processed']
        widgets = {
            'response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите ваш ответ на отзыв...'
            }),
            'is_processed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'response': 'Ответ на отзыв',
            'is_processed': 'Отметить как обработанный'
        }
