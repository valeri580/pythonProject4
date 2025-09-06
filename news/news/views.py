from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.base import ContentFile
from datetime import datetime
import requests
from .models import News_post, Like, PendingNews, Favorite
from .forms import CustomUserCreationForm, NewsApprovalForm, LoadNewsForm
from .services import NewsScrapingService

# Create your views here.

@ensure_csrf_cookie
def news_home(request):
	news = News_post.objects.filter(is_approved=True).prefetch_related('images').order_by('-pub_date')
	return render(request, 'news_home.html', {'news': news})

def news_detail(request, news_id):
	post = get_object_or_404(News_post.objects.prefetch_related('images'), id=news_id, is_approved=True)
	is_liked = False
	is_favorited = False
	if request.user.is_authenticated:
		is_liked = Like.objects.filter(user=request.user, news_post=post).exists()
		is_favorited = Favorite.objects.filter(user=request.user, news_post=post).exists()
	context = {
		'post': post,
		'is_liked': is_liked,
		'is_favorited': is_favorited,
	}
	return render(request, 'news_detail.html', context)

def home(request):
	return render(request, 'home.html')

def page2(request):
	return render(request, 'page2.html')

def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Аккаунт для {username} успешно создан! Теперь вы можете войти.')
			return redirect('login')
	else:
		form = CustomUserCreationForm()
	return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'registration/profile.html')

@login_required
@require_POST
def toggle_like(request, news_id):
	news_post = get_object_or_404(News_post, id=news_id)
	
	# Проверяем, лайкнул ли пользователь уже эту новость
	like, created = Like.objects.get_or_create(
		user=request.user,
		news_post=news_post
	)
	
	if not created:
		# Если лайк уже был, удаляем его (убираем лайк)
		like.delete()
		
	# Пересчитываем факт лайка для надежности
	liked = Like.objects.filter(user=request.user, news_post=news_post).exists()
	
	# Возвращаем JSON ответ для AJAX
	from .models import Like as LikeModel
	total = LikeModel.objects.filter(news_post=news_post).count()
	return JsonResponse({
		'liked': liked,
		'total_likes': total
	})

@login_required
@require_POST
def toggle_favorite(request, news_id):
	news_post = get_object_or_404(News_post, id=news_id)
	fav, created = Favorite.objects.get_or_create(user=request.user, news_post=news_post)
	if not created:
		fav.delete()
		favorited = False
	else:
		favorited = True
	return JsonResponse({'favorited': favorited})

@login_required
def favorites_list(request):
	posts = News_post.objects.filter(favorited_by__user=request.user, is_approved=True).prefetch_related('images').order_by('-pub_date')
	return render(request, 'favorites.html', {'news': posts})

def image_proxy(request):
	"""Прокси для безопасной загрузки внешних изображений по URL."""
	url = request.GET.get('url')
	if not url:
		return HttpResponseBadRequest('Missing url')
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
			'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
			'Referer': 'https://example.com/'
		}
		resp = requests.get(url, headers=headers, timeout=10)
		if resp.status_code != 200 or not resp.content:
			raise ValueError('bad status')
		content_type = resp.headers.get('Content-Type', 'image/jpeg')
		return HttpResponse(resp.content, content_type=content_type)
	except Exception:
		placeholder_svg = (
			"<svg xmlns='http://www.w3.org/2000/svg' width='600' height='250'>"
			"<rect fill='#e9ecef' width='100%' height='100%'/>"
			"<text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='#6c757d' font-size='24'>Нет изображения</text>"
			"</svg>"
		)
		return HttpResponse(placeholder_svg, content_type='image/svg+xml')

@staff_member_required
def admin_load_news(request):
	"""Админ-панель для загрузки новостей из интернета"""
	if request.method == 'POST':
		form = LoadNewsForm(request.POST)
		if form.is_valid():
			count = form.cleaned_data['count']
			scraping_service = NewsScrapingService()
			
			try:
				loaded_news = scraping_service.load_news_batch(request.user, count)
				messages.success(
					request, 
					f'Успешно загружено {len(loaded_news)} новостей для модерации!'
				)
			except Exception as e:
				messages.error(request, f'Ошибка при загрузке новостей: {e}')
			
			return redirect('admin_pending_news')
	else:
		form = LoadNewsForm()
	
	return render(request, 'admin/load_news.html', {'form': form})

@staff_member_required 
def admin_pending_news(request):
	"""Список новостей на модерации"""
	pending_news = PendingNews.objects.filter(is_processed=False).order_by('-created_at')
	return render(request, 'admin/pending_news.html', {'pending_news': pending_news})

@staff_member_required
def admin_approve_news(request, news_id):
	"""Форма для одобрения/редактирования новости"""
	pending_news = get_object_or_404(PendingNews, id=news_id, is_processed=False)
	
	if request.method == 'POST':
		form = NewsApprovalForm(request.POST)
		if form.is_valid():
			if form.cleaned_data.get('approve'):
				# Создаем новость
				news_post = News_post.objects.create(
					title=form.cleaned_data['title'],
					short_description=form.cleaned_data['short_description'],
					text=form.cleaned_data['text'],
					author=form.cleaned_data['author'],
					pub_date=datetime.now(),
					source_url=pending_news.source_url,
					is_approved=True,
					is_from_internet=True
				)
				
				# Сохраняем URL изображения (если отсутствует — подставим плейсхолдер)
				news_post.image = pending_news.image_url or ''
				news_post.save(update_fields=['image'])
				
				messages.success(request, f'Новость "{news_post.title}" успешно опубликована!')
			else:
				messages.info(request, 'Новость отклонена.')
			
			# Помечаем как обработанную
			pending_news.is_processed = True
			pending_news.save()
			
			return redirect('admin_pending_news')
	else:
		# Предзаполняем форму данными из загруженной новости
		form = NewsApprovalForm(initial={
			'title': pending_news.title,
			'short_description': pending_news.short_description,
			'text': pending_news.text,
			'author': request.user,  # По умолчанию текущий пользователь
		})
	
	return render(request, 'admin/approve_news.html', {
		'form': form,
		'pending_news': pending_news
	})
