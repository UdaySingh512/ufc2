# Generated by Django 4.0.3 on 2022-05-19 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0027_delete_videos'),
    ]

    operations = [
        migrations.DeleteModel(
            name='recordings',
        ),
    ]