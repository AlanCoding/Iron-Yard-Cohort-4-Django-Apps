from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
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
