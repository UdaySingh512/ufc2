# Generated by Django 4.0.3 on 2022-03-29 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0011_athletes_age_athletes_height_athletes_ko_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='league',
        ),
        migrations.AddField(
            model_name='match',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='athletes',
            name='facebook',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='league',
        ),
    ]
