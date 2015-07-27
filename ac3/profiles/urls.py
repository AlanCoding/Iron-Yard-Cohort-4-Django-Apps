from django.conf.urls import include, patterns, url
from django.contrib import admin
from profiles import views as prof_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^register.html$', prof_views.view_register, name="view_register"),
    url(r'^logout.html$', prof_views.view_logout, name="view_logout"),
    url(r'^login.html$', prof_views.view_login, name="view_login"),

    # url('^', include('django.contrib.auth.urls'))

]
