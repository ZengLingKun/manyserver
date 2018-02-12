# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Oserver', '0004_auto_20180212_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='host_ip',
            field=models.GenericIPAddressField(unique=True),
        ),
    ]
