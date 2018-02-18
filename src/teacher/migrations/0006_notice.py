# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-18 08:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20180211_0022'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacher', '0005_auto_20180211_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_class', to='account.Class')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_school', to='account.School')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_notice', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]