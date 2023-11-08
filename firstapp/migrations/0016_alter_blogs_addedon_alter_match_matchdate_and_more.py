# Generated by Django 4.0.3 on 2022-04-15 07:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0015_athletes_bannerimage_alter_blogs_addedon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='addedon',
            field=models.DateField(default=datetime.date(2022, 4, 15)),
        ),
        migrations.AlterField(
            model_name='match',
            name='matchDate',
            field=models.DateField(default=datetime.date(2022, 4, 15)),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(default=datetime.date(2022, 4, 15)),
        ),
        migrations.AlterField(
            model_name='registeredusers',
            name='registerDate',
            field=models.DateField(default=datetime.date(2022, 4, 15)),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='reviewDate',
            field=models.DateField(default=datetime.date(2022, 4, 15)),
        ),
        migrations.AlterField(
            model_name='stories',
            name='date',
            field=models.DateField(default=datetime.date(2022, 4, 15)),
        ),
    ]