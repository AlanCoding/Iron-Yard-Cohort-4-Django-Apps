"""movieratings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, patterns, url
from django.contrib import admin
from movies import views as movie_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^$', movie_views.view_index, name="view_index"),
    url(r'^user.html([\d]+)$', movie_views.UserView.as_view(), name="view_user"),
    url(r'^movie.html(?P<movie_id>\d+)$', movie_views.view_movie, name="view_movie"),
    url(r'^rating.html(?P<rating_id>\d+)$', movie_views.view_rating, name="view_rating"),
    url(r'^dashboard.html$', movie_views.view_dashboard, name="view_dashboard"),
    url(r'^fig(?P<movie_id>\d+).png$', movie_views.view_fig, name="view_fig"),
    url(r'^genre.html(?P<genre_id>\d+)$', movie_views.GenreView.as_view(), name="view_genre"),
    url(r'^top20.html$', movie_views.Top20View.as_view(), name="top_rated_movies"),

]
