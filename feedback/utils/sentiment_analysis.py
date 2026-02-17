"""
Модуль для анализа тональности отзывов (sentiment analysis)
Простой rule-based подход на основе ключевых слов и оценки
"""


def analyze_sentiment(text, rating):
    """
    Анализирует тональность текста отзыва
    
    Args:
        text (str): Текст отзыва
        rating (int): Оценка от 1 до 5
    
    Returns:
        str: POSITIVE, NEUTRAL или NEGATIVE
    """
    text_lower = text.lower()
    
    # Ключевые слова для определения тональности
    positive_keywords = [
        'отличн', 'прекрасн', 'замечательн', 'великолепн', 'супер', 'класс',
        'хорош', 'нравится', 'понравил', 'рекомендую', 'качественн',
        'быстр', 'вежлив', 'доволен', 'спасибо', 'благодар', 'молодц',
        'профессионал', 'идеальн', 'восхитительн', 'превосходн'
    ]
    
    negative_keywords = [
        'плох', 'ужасн', 'отвратительн', 'кошмар', 'разочаров',
        'не рекомендую', 'недоволен', 'жалоб', 'претензи', 'проблем',
        'медленн', 'грубост', 'невежлив', 'некачественн', 'обман',
        'разорван', 'сломан', 'испорчен', 'бракован', 'задержк'
    ]
    
    # Подсчет позитивных и негативных слов
    positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
    negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
    
    # Определение тональности на основе рейтинга и ключевых слов
    if rating >= 4:
        if negative_count > positive_count:
            return 'NEUTRAL'
        return 'POSITIVE'
    elif rating <= 2:
        if positive_count > negative_count:
            return 'NEUTRAL'
        return 'NEGATIVE'
    else:  # rating == 3
        if positive_count > negative_count:
            return 'POSITIVE'
        elif negative_count > positive_count:
            return 'NEGATIVE'
        return 'NEUTRAL'
