"""urly_bird URL Configuration

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
from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import routers

from urly import views as v
from urly import models as m

from profiles.models import Profile


router = routers.DefaultRouter()
router.register(r'bmks', v.BookmarkViewSet)
router.register(r'clk',  v.ClickViewSet)
router.register(r'usr',  v.BookmarkerViewSet)


urlpatterns = [
    # API Pages
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
            # lower level views in API-land
    url(r'^usr/(?P<bmkr_id>\d+)/bmks/', v.BookmarkerBookmarkList.as_view(), name="bookmarker-bookmark"),
    url(r'^bmks/(?P<bmk_id>\d+)/clicks/', v.BookmarkClickList.as_view(), name="bookmark-click"),

    # App pages
    url(r'^accounts/profile', v.BookmarkerView.as_view(), name='dashboard'),
    # my pages
    url(r'^index.html$', v.IndexPageView.as_view(), name='view_index'),
    url(r'^(?P<code>\w+)$', v.ClickView.as_view(), name='click'),
    url(r'^u/(?P<user_id>\d+)$', v.BookmarkerView.as_view(), name='bookmarker'),
    url(r'^b/(?P<code>\w+)$', v.BookmarkView.as_view(), name='bookmark'),
    url(r'^bmk_list.html$', ListView.as_view(
                    model=m.Bookmark,
                    template_name="lists/bmk_list.html",
                    context_object_name='bookmarks',
                    paginate_by=10
                    ), name='bmk_list'),

    url(r'^usr_list.html$', ListView.as_view(
                    model=Profile,
                    template_name="lists/usr_list.html",
                    context_object_name='bookmarkers',
                    paginate_by=10
                    ), name='usr_list'),
]
