# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Oserver', '0003_server_has_nmon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='body',
            field=models.TextField(null=True, blank=True),
        ),
    ]
