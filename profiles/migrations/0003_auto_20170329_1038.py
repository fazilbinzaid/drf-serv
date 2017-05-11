# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170313_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_ctc',
            field=models.DecimalField(decimal_places=2, max_digits=3, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='designation',
            field=models.CharField(max_length=20, choices=[('Project Manager', 'Project Manager'), ('Developer', 'Developer'), ('Tester', 'Tester'), ('Technical Lead', 'Technical Lead'), ('Hybrid', 'Hybrid'), ('DevOps', 'DevOps'), ('Fresher', 'Fresher'), ('Project Coordinator', 'Project Coordinator'), ('UI/UX Designer', 'UI/UX Designer'), ('UI/UX Developer', 'UI/UX Developer'), ('HTML Developer', 'HTML Developer')], blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='expected_ctc',
            field=models.DecimalField(decimal_places=2, max_digits=3, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='notice_period',
            field=models.IntegerField(blank=True, default=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='recording_optional',
            field=models.FileField(upload_to='media/', blank=True),
        ),
    ]
