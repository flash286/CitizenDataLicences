# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_owner_contract_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='contract_abi',
            field=models.TextField(default=b''),
        ),
    ]
