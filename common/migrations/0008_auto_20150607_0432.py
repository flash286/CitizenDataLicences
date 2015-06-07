# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_owner_contract_addr'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='fee',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='owner',
            name='contract_abi',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='owner',
            name='contract_addr',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='owner',
            name='contract_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'HOLD'), (2, 'SUCCESS'), (3, 'FAIL'), (4, 'OUT_OF_DATE')]),
        ),
    ]
