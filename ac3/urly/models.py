from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
import datetime

from django.utils import timezone
import pytz
from django.conf import settings


# static functions
def generate_code():
    from random import choice
    from string import ascii_lowercase
    return "".join(choice(ascii_lowercase) for _ in range(4))

# managers
class BookmarkManager(models.Manager):
	def allocate_code(self):
	    while True:
	        try_code = generate_code()
	        if not self.code_duplicate(try_code):
	            break
	    return try_code

	def code_duplicate(self, code):
	    ret = False
	    for b in self.all():
	        if code == b.code:
	            ret = True
	            break
	    return ret

# models
class Tag(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Bookmark(models.Model):
    URL = models.URLField(max_length=300)
    code = models.CharField(max_length=10, unique=True)
    posted_at = models.DateTimeField(blank=True, auto_now=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User)
#    user = models.ForeignKey(User, null=True)

    tag = models.ManyToManyField(Tag, blank=True)

    objects = BookmarkManager()

    def __str__(self):
        ret_st = ""
        if self.title is None:
            ret_st += self.title + ": "
        ret_st += self.URL
        return ret_st

    def total_clicks(self):
        return len(self.click_set.all())

    def print_url(self):
        if len(self.URL) > 50:
            return self.URL[:47] + "..."
        else:
            return self.URL


class Click(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    user = models.ForeignKey(User, null=True)
    clicked_at = models.DateTimeField(null=True, auto_now=True)

    def set_time(self):
        timezone.activate(settings.TIME_ZONE)
        now_t = timezone.now()
        self.clicked_at = timezone.now()
        timezone.deactivate()
