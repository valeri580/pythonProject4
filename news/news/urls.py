from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('page2/', views.page2, name='page2'),
    path('news/', views.news_home, name='news_home'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    
    # Лайки
    path('news/<int:news_id>/like/', views.toggle_like, name='toggle_like'),
    path('news/<int:news_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    # Прокси изображений
    path('image-proxy/', views.image_proxy, name='image_proxy'),
    
    # Админ-функции для загрузки новостей
    path('admin-panel/load-news/', views.admin_load_news, name='admin_load_news'),
    path('admin-panel/pending-news/', views.admin_pending_news, name='admin_pending_news'),
    path('admin-panel/approve-news/<int:news_id>/', views.admin_approve_news, name='admin_approve_news'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        authentication_form=CustomAuthenticationForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('favorites/', views.favorites_list, name='favorites_list'),
]
