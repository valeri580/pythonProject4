from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class News_post(models.Model):
	title = models.CharField('Название новости', max_length=200)
	short_description = models.CharField('Краткое описание новости', max_length=300)
	text = models.TextField('Новость')
	pub_date = models.DateTimeField('Дата публикации')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	image = models.CharField('Изображение (URL)', max_length=500, blank=True, null=True)
	source_url = models.URLField('URL источника', blank=True, null=True)
	is_approved = models.BooleanField('Одобрено', default=False)
	is_from_internet = models.BooleanField('Загружено из интернета', default=False)
	likes = models.ManyToManyField(User, through='Like', related_name='liked_posts', blank=True)
	
	def __str__(self):
		return self.title
	
	def total_likes(self):
		return self.likes.count()
	
	def is_liked_by(self, user):
		if user.is_authenticated:
			return self.likes.filter(id=user.id).exists()
		return False
	
	class Meta:
		verbose_name = 'Новость'
		verbose_name_plural = 'Новости'


class PendingNews(models.Model):
	title = models.CharField('Название новости', max_length=200)
	short_description = models.CharField('Краткое описание новости', max_length=300)
	text = models.TextField('Текст новости')
	source_url = models.URLField('URL источника')
	image_url = models.URLField('URL изображения', blank=True, null=True)
	created_at = models.DateTimeField('Дата загрузки', auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Загружено пользователем')
	is_processed = models.BooleanField('Обработано', default=False)
	
	class Meta:
		verbose_name = 'Новость на модерации'
		verbose_name_plural = 'Новости на модерации'
		ordering = ['-created_at']
	
	def __str__(self):
		return f'{self.title} (ожидает модерации)'


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	news_post = models.ForeignKey(News_post, on_delete=models.CASCADE, verbose_name='Новость')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата лайка')
	
	class Meta:
		unique_together = ('user', 'news_post')
		verbose_name = 'Лайк'
		verbose_name_plural = 'Лайки'
	
	def __str__(self):
		return f'{self.user.username} лайкнул "{self.news_post.title}"'


class NewsImage(models.Model):
	news_post = models.ForeignKey(News_post, on_delete=models.CASCADE, related_name='images', verbose_name='Новость')
	image_url = models.URLField('URL изображения', max_length=500)
	created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

	class Meta:
		verbose_name = 'Изображение новости'
		verbose_name_plural = 'Изображения новости'
		ordering = ['id']

	def __str__(self):
		return f'Изображение для: {self.news_post.title}'


class Favorite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Пользователь')
	news_post = models.ForeignKey(News_post, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Новость')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

	class Meta:
		unique_together = ('user', 'news_post')
		verbose_name = 'Избранное'
		verbose_name_plural = 'Избранные'

	def __str__(self):
		return f'{self.user.username} добавил в избранное "{self.news_post.title}"'
