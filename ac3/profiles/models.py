from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg
import datetime
import pytz


class ProgBar:
    text = ""
    val = 0
    def __init__(self, text, val):
        self.text = text
        self.val = val


class Profile(models.Model):
	creation_date = models.DateTimeField(auto_now=True)
	user = models.OneToOneField(User)

	def __str__(self):
		return str(self.user)

class Rater(models.Model):
    age = models.IntegerField(default=0, blank=True, null=True)
    gender_options = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=gender_options, default='M', blank=True, null=True)
    occupation_options = (
    	( 0, "other"),
    	( 1, "academic/educator"),
    	( 2, "artist"),
    	( 3, "clerical/admin"),
    	( 4, "college/grad student"),
    	( 5, "customer service"),
    	( 6, "doctor/health care"),
    	( 7, "executive/managerial"),
    	( 8, "farmer"),
    	( 9, "homemaker"),
    	(10, "K-12 student"),
    	(11, "lawyer"),
    	(12, "programmer"),
    	(13, "retired"),
    	(14, "sales/marketing"),
    	(15, "scientist"),
    	(16, "self-employed"),
    	(17, "technician/engineer"),
    	(18, "tradesman/craftsman"),
    	(19, "unemployed"),
    	(20,  "writer") )
    occupation = models.IntegerField(choices=occupation_options, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)#, default="00000)

    user = models.OneToOneField(User, blank=True, null=True) # added for user accounts

    def greeting(self):
        if self.gender == "M":
            return "his"
        else:
            return "her"

    def rating_count(self):
        return self.rating_set.count()

    def prior_user(self):
        i = self.id - 1
        if i < 1:
            i = 1
        return i

    def next_user(self):
        i = self.id + 1
        if i > len(Rater.objects.all()):
            i = len(Rater.objects.all())
        return i

    def avg_rating(self):
        r_set = self.rating_set.all()
        if len(r_set) == 0:
            return 0
        else:
            dict = r_set.aggregate(Avg('rating'))
            return round(dict["rating__avg"], 2)

    def has_rated(self, movie):
        for r in self.rating_set.all():
            if r.movie == movie:
                return True
        return False

    def star_hist(self):
        hist = [0 for i in range(5)]
        for r in self.rating_set.all():
            hist[r.rating-1] += 1
        star_max = 50
        if max(hist) > star_max:
            h_max = max(hist)
            for i in range(5):
                hist[i] = int(star_max*hist[i]/h_max)
        s = ["" for i in range(5)]
        for i in range(5):
            s[i] = str(i+1)+" star: "+"#"*hist[i]
        return s


    def star_numbs(self):
        hist = [0 for i in range(5)]
        for r in self.rating_set.all():
            hist[r.rating-1] += 1
        star_max = 100
        if max(hist) > star_max:
            h_max = max(hist)
            for i in range(5):
                hist[i] = int(star_max*hist[i]/h_max)
        ret_prog = [None for i in range(5)]
        for i in range(5):
            in_text = " " + "*"*(i+1)
            ret_prog[i] = ProgBar(text=in_text, val=hist[i])
        return ret_prog


    def __str__(self):
        return "user #"+str(self.pk).ljust(5)+" with "+\
                str(self.rating_set.count())+" reviews"
