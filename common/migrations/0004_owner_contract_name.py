# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20150531_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='contract_name',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
