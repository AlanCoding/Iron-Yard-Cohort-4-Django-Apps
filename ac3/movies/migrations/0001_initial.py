# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('text', models.CharField(default='', max_length=300)),
                ('Nratings_save', models.IntegerField(null=True)),
                ('Nmovies_save', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(default='unknown', max_length=200)),
                ('release_date', models.IntegerField(default=1990)),
                ('avg_save', models.FloatField(null=True)),
                ('total_save', models.IntegerField(null=True)),
                ('genre', models.ManyToManyField(to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('posted', models.IntegerField(default=0)),
                ('review', models.TextField(null=True)),
                ('rating', models.IntegerField(choices=[(1, '*'), (2, '**'), (3, '***'), (4, '****'), (5, '*****')], default=1)),
                ('movie', models.ForeignKey(default=1, to='movies.Movie')),
                ('rater', models.ForeignKey(default=1, to='profiles.Rater')),
            ],
        ),
    ]
