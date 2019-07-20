# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-19 19:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0006_list_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='shared_with',
            field=models.ManyToManyField(blank=True, null=True, related_name='shared', to=settings.AUTH_USER_MODEL),
        ),
    ]