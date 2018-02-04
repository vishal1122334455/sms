# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-03 21:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0012_subject'),
        ('office', '0004_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='GallaryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(blank=True, default='no-img.jpg', null=True, upload_to='school/gallary/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.School')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]