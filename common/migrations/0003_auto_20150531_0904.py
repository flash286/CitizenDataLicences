# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150531_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='contract_code_lll',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='owner',
            name='contract_code_pretty',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
