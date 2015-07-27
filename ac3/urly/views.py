from .models import Bookmark, Tag, Click
from .forms import BookmarkForm, BookmarkerForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import django.views.generic as views

from django.views.generic.edit import CreateView
from django.conf import settings

from django.contrib.auth.models import User

from django.utils import timezone
import pytz

# for viewset stuff
from rest_framework import viewsets, permissions, generics, filters
import urly.serializer as ser
import urly.permissions as per
from django.views.decorators.http import require_http_methods
import django_filters

from profiles.models import Profile


class BookmarkerFilter(django_filters.FilterSet):
    # age = django_filters.IntegerFilter(name="age", lookup_type="icontains")
    gender = django_filters.CharFilter(name="gender", lookup_type="icontains")
    # notes = django_filters.CharFilter(name="notes", lookup_type="icontains")

    class Meta:
        model = Profile
        fields = [ 'gender',]

# view sets

# @require_http_methods(["GET", "PUT", "DELETE", "POST"])
class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ser.BookmarkSerializer
    queryset = Bookmark.objects.all()

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 5
        return 20

class ClickViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Click.objects.all()
    serializer_class = ser.ClickSerializer

class BookmarkerViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ser.BookmarkerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BookmarkerFilter

# lower level in API

class BookmarkerBookmarkList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ser.BookmarkSerializer

    def initial(self, request, *args, **kwargs):
        self.Profile = Profile.objects.get(pk=kwargs['bmkr_id'])
        self.user = self.profile.user
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return self.user.bookmark_set

    def perform_create(self, serializer):
        usr = self.request.user
        if usr != self.user:
            raise PermissionDenied

        timezone.activate(settings.TIME_ZONE)
        now_t = timezone.now()
        timezone.deactivate()

        the_code = Bookmark.objects.allocate_code()

        serializer.save(posted_at=now_t, user=self.user, code=the_code)


class BookmarkClickList(generics.ListCreateAPIView):
    serializer_class = ser.ClickSerializer

    def initial(self, request, *args, **kwargs):
        self.bookmark = Bookmark.objects.get(pk=kwargs['bmk_id'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return self.bookmark.click_set

    def perform_create(self, serializer):
        timezone.activate(settings.TIME_ZONE)
        now_t = timezone.now()
        timezone.deactivate()
        serializer.save(bookmark=self.bookmark, user=self.request.user, clicked_at=now_t)


class BookmarkerView(views.ListView):
    template_name = 'urly/bookmarker.html'
#    model = Bookmark
    paginate_by = 20
    context_object_name = 'bookmarks'
    profile = None

    def dispatch(self, *args, **kwargs):
        if 'user_id' in self.kwargs:
            self.profile = Profile.objects.get(pk=self.kwargs['user_id'])
        else:
            self.profile = self.request.user.profile
        return super(BookmarkerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.profile.user.bookmark_set.order_by('-posted_at')

    def get_context_data(self, **kwargs):
        context = super(BookmarkerView, self).get_context_data(**kwargs)
        context['bookmarker'] = self.profile
        return context


class IndexPageView(views.CreateView):
    template_name = 'urly/index.html'
    model = Bookmark
    # fields = ['URL', 'title', 'description']
    form_class = BookmarkForm
    success_url = 'urly/index.html'

    def form_valid(self, form):
        timezone.activate(settings.TIME_ZONE)
        now_t = timezone.now()
        timezone.deactivate()

        form.instance.posted_at = now_t
        form.instance.code = Bookmark.objects.allocate_code()
        user = self.request.user

        if user is not None and user.is_authenticated():
            form.instance.user = user
        else:
            form.instance.user = User.objects.get(pk=1)
        messages.add_message(self.request, messages.SUCCESS,
                            "Your bookmark has been added!!1")
        return super(IndexPageView, self).form_valid(form)


class ClickView(views.RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'click_view_redirect'
    url = 'http://www.google.com' # if approach fails

    def get_redirect_url(self, *args, **kwargs):
        bookmark = Bookmark.objects.get(code=kwargs['code'])
        click = Click(bookmark=bookmark)
        click.set_time()
        click.save()
        self.url = bookmark.URL
        return super(ClickView, self).get_redirect_url(*args, **kwargs)


class BookmarkView(views.ListView):
    template_name = 'urly/bookmark.html'
    model = Bookmark
    context_object_name = 'clicks'
    bmk = None

    def get_queryset(self):
        self.bmk = Bookmark.objects.get(code=self.kwargs['code'])
        return self.bmk.click_set.all()

    def get_context_data(self, **kwargs):
        context = super(BookmarkView, self).get_context_data(**kwargs)
        context['bookmark'] = self.bmk
        return context
