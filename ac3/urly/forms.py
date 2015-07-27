from django import forms
from django.contrib.auth.models import User
from urly.models import Bookmark, Click
from profiles.models import Profile

class BookmarkForm(forms.ModelForm):

    class Meta:
        model = Bookmark
        fields = ('URL', 'title', 'description',)
#        blank = True

class BookmarkerForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('age', 'gender')
