from django import forms
from django.contrib.auth.models import User
from movies.models import Rating
from profiles.models import Rater
# Profile

class RaterForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ('age', 'gender', 'occupation', 'zip_code',)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating', 'review',)
