from django.conf.urls import include, patterns, url
from django.contrib import admin
from profiles import views as prof_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^register.html$', prof_views.view_register, name="view_register"),
    url(r'^logout.html$', prof_views.view_logout, name="view_logout"),
    url(r'^login.html$', 'django.contrib.auth.views.login', name="view_login"),
    url(r'^edit.html$', prof_views.edit_user, name="edit_user"),
    # global user info views
    url(r'^users/$', prof_views.ListUsersView.as_view(), name="view_users"),
    url(r'^user/(?P<pk>\d+)$', prof_views.UserDetailView.as_view(), name="view_user"),

    # url('^', include('django.contrib.auth.urls'))

]
