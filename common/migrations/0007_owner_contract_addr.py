# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_owner_contract_deployed'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='contract_addr',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
