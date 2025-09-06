from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Movie


@require_http_methods(["GET", "POST"])
def movie_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        review = request.POST.get("review", "").strip()
        if title:
            Movie.objects.create(title=title, description=description, review=review)
            return redirect(reverse("movie_list"))
    return render(request, "films/movie_form.html")


def movie_list(request):
    movies = Movie.objects.order_by("-created_at")
    return render(request, "films/movie_list.html", {"movies": movies})
