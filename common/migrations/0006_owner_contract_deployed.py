# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_owner_contract_abi'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='contract_deployed',
            field=models.BooleanField(default=False),
        ),
    ]
