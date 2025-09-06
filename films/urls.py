from django.urls import path

from . import views


urlpatterns = [
    path('', views.movie_create, name='movie_create'),
    path('list/', views.movie_list, name='movie_list'),
]


