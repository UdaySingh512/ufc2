# Generated by Django 4.0.3 on 2022-03-16 06:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_registeredusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('reviewDate', models.DateField(default=datetime.date(2022, 3, 16))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.registeredusers')),
            ],
        ),
    ]
