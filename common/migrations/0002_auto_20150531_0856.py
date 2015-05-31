# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='timestamp',
            field=models.DateTimeField(db_index=True),
        ),
    ]
