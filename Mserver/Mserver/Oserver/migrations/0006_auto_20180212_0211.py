# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Oserver', '0005_auto_20180212_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='where_add',
            field=models.CharField(default=b'admin', max_length=50),
        ),
        migrations.AlterField(
            model_name='server',
            name='host_passwd',
            field=models.CharField(default=b'ops123!', max_length=50),
        ),
        migrations.AlterField(
            model_name='server',
            name='host_user',
            field=models.CharField(default=b'root', max_length=50),
        ),
    ]
