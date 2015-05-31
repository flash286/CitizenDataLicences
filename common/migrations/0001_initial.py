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
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('balance', models.FloatField()),
                ('block_chain_account', models.CharField(max_length=255)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(related_name='sensors', to='common.Owner')),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('value', models.FloatField()),
                ('sensor', models.ForeignKey(related_name='data', to='common.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_id', models.CharField(max_length=255)),
                ('cost', models.PositiveIntegerField(default=0)),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(1, b'HOLD'), (2, b'SUCCESS'), (3, b'FAIL'), (4, b'OUT_OF_DATE')])),
                ('dt_start', models.PositiveIntegerField(default=0)),
                ('dt_end', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
