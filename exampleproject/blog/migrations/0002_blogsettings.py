# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_vest.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('current_theme', django_vest.fields.VestField(max_length=125, choices=[(b'dark_theme', b'dark_theme'), (b'main_theme', b'main_theme')])),
            ],
            options={
                'verbose_name': 'blog settings',
                'verbose_name_plural': 'blog settings',
            },
            bases=(models.Model,),
        ),
    ]
