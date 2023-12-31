# Generated by Django 4.0.3 on 2022-03-17 06:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_alter_athletes_image_alter_news_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='league',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stadium', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchDate', models.DateField(default=datetime.date(2022, 3, 17))),
                ('matchTime', models.TimeField()),
                ('athlete1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.athletes')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.league')),
            ],
        ),
        migrations.CreateModel(
            name='stories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('content', models.TextField()),
                ('date', models.DateField(default=datetime.date(2022, 3, 17))),
            ],
        ),
        migrations.CreateModel(
            name='videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.match')),
            ],
        ),
        migrations.CreateModel(
            name='recordings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video', models.FileField(upload_to='')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.match')),
            ],
        ),
        migrations.CreateModel(
            name='gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.match')),
            ],
        ),
    ]
