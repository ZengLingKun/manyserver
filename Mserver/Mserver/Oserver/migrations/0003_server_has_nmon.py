# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Oserver', '0002_auto_20171213_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='has_nmon',
            field=models.BooleanField(default=0),
        ),
    ]
