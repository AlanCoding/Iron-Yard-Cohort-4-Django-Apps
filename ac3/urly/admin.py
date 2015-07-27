from django.contrib import admin
from urly.models import *
from profiles.models import Profile

# Register your models here.
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'URL', 'code', "posted_at", "title", "description"]

class BookmarkerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'age', 'gender']

class TagAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'text']

class ClickAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'user', 'clicked_at']

# Register your models here.
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Profile, BookmarkerAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Click, ClickAdmin)
