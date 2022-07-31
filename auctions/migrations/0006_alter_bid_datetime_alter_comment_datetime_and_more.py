# Generated by Django 4.0.4 on 2022-07-31 12:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bid_datetime_alter_comment_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 31, 12, 42, 20, 356769, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 31, 12, 42, 20, 357065, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 31, 12, 42, 20, 355980, tzinfo=utc)),
        ),
    ]