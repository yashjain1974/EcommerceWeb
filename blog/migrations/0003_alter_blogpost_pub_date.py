# Generated by Django 4.0 on 2022-02-03 18:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_content_head0_blogpost_content_head1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 2, 3, 18, 3, 40, 679119, tzinfo=utc)),
        ),
    ]