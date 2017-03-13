# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import profiles.managers


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', blank=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', profiles.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('designation', models.CharField(max_length=20, choices=[('Project Manager', 'Project Manager'), ('Developer', 'Developer'), ('Tester', 'Tester'), ('Technical Lead', 'Technical Lead'), ('Hybrid', 'Hybrid'), ('DevOps', 'DevOps'), ('Fresher', 'Fresher'), ('Project Coordinator', 'Project Coordinator'), ('UI/UX Designer', 'UI/UX Designer'), ('UI/UX Developer', 'UI/UX Developer'), ('HTML Developer', 'HTML Developer')])),
                ('location', models.CharField(max_length=20)),
                ('current_ctc', models.DecimalField(max_digits=3, decimal_places=2)),
                ('expected_ctc', models.DecimalField(max_digits=3, decimal_places=2)),
                ('notice_period', models.IntegerField()),
                ('resume', models.FileField(upload_to='docs/', blank=True)),
                ('recording', models.FileField(upload_to='media/', blank=True)),
                ('recording_optional', models.FileField(upload_to='', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='profiles')),
            ],
        ),
        migrations.CreateModel(
            name='Skillset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('skill', models.CharField(max_length=10)),
                ('exp', models.IntegerField()),
                ('profile', models.ForeignKey(to='profiles.Profile', related_name='skills')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='skillset',
            unique_together=set([('profile', 'skill')]),
        ),
    ]
