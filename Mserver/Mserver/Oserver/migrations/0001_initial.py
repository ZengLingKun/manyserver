# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_ip', models.IPAddressField()),
                ('host_user', models.CharField(max_length=50)),
                ('host_passwd', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('host_os', models.CharField(default=b'l', max_length=50, choices=[(b'w', b'Windowns'), (b'l', b'RedHat')])),
                ('category', models.ForeignKey(related_name='host_category', to='Oserver.Category')),
            ],
            options={
                'ordering': ('category', '-host_ip'),
            },
        ),
    ]
