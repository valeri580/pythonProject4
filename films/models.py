from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название фильма')
    description = models.TextField(blank=True, verbose_name='Описание фильма')
    review = models.TextField(blank=True, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
