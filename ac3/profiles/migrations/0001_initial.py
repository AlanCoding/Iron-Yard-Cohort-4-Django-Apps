# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('age', models.IntegerField(default=0, null=True, blank=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', blank=True, null=True, max_length=1)),
                ('occupation', models.IntegerField(choices=[(0, 'other'), (1, 'academic/educator'), (2, 'artist'), (3, 'clerical/admin'), (4, 'college/grad student'), (5, 'customer service'), (6, 'doctor/health care'), (7, 'executive/managerial'), (8, 'farmer'), (9, 'homemaker'), (10, 'K-12 student'), (11, 'lawyer'), (12, 'programmer'), (13, 'retired'), (14, 'sales/marketing'), (15, 'scientist'), (16, 'self-employed'), (17, 'technician/engineer'), (18, 'tradesman/craftsman'), (19, 'unemployed'), (20, 'writer')], null=True, blank=True)),
                ('zip_code', models.CharField(null=True, blank=True, max_length=10)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
    ]
