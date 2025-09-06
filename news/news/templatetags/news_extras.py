from django import template
from news.models import Favorite

register = template.Library()

@register.filter
def is_liked_by(news_post, user):
    """Проверяет, лайкнул ли пользователь новость"""
    return news_post.is_liked_by(user)

@register.filter
def is_favorited_by(news_post, user):
    """Проверяет, находится ли новость в избранном у пользователя"""
    if not getattr(user, 'is_authenticated', False):
        return False
    return Favorite.objects.filter(user=user, news_post=news_post).exists()
