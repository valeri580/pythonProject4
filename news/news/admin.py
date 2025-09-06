from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import News_post, Like, PendingNews

# Register your models here.

@admin.register(News_post)
class NewsPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'pub_date', 'is_approved', 'is_from_internet', 'total_likes')
	list_filter = ('pub_date', 'author', 'is_approved', 'is_from_internet')
	search_fields = ('title', 'short_description')
	date_hierarchy = 'pub_date'
	readonly_fields = ('total_likes',)
	
	fieldsets = (
		('Основная информация', {
			'fields': ('title', 'short_description', 'text', 'image')
		}),
		('Публикация', {
			'fields': ('author', 'pub_date', 'is_approved')
		}),
		('Дополнительно', {
			'fields': ('source_url', 'is_from_internet', 'total_likes'),
			'classes': ('collapse',)
		})
	)

@admin.register(PendingNews)
class PendingNewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_by', 'created_at', 'is_processed', 'approve_link')
	list_filter = ('created_at', 'is_processed', 'created_by')
	search_fields = ('title', 'short_description')
	readonly_fields = ('created_at', 'created_by')
	
	def approve_link(self, obj):
		if not obj.is_processed:
			url = reverse('admin_approve_news', args=[obj.id])
			return format_html('<a href="{}" class="button">Модерировать</a>', url)
		return "Обработано"
	approve_link.short_description = 'Действия'
	
	def get_queryset(self, request):
		return super().get_queryset(request).select_related('created_by')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
	list_display = ('user', 'news_post', 'created_at')
	list_filter = ('created_at', 'news_post')
	search_fields = ('user__username', 'news_post__title')


# Добавляем кастомные админ-действия
class CustomAdminSite(admin.AdminSite):
	site_header = 'Админ-панель новостного сайта'
	site_title = 'Новости'
	index_title = 'Управление новостным сайтом'
	
	def each_context(self, request):
		context = super().each_context(request)
		if request.user.is_staff:
			context['custom_links'] = [
				{
					'title': '📥 Загрузить новости из интернета',
					'url': reverse('admin_load_news'),
					'description': 'Загрузить новости по теме нейросети'
				},
				{
					'title': '📋 Новости на модерации',
					'url': reverse('admin_pending_news'), 
					'description': 'Просмотр и одобрение загруженных новостей'
				}
			]
		return context

# Переопределяем стандартную админку
admin.site.__class__ = CustomAdminSite
