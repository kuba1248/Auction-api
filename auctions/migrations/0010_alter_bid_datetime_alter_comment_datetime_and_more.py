# Generated by Django 4.0.4 on 2022-07-31 13:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_datetime_alter_comment_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 31, 13, 11, 41, 100050, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 31, 13, 11, 41, 100358, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='end_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 31, 13, 11, 41, 99226, tzinfo=utc)),
        ),
    ]