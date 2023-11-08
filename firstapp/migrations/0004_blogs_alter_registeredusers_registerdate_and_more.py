# Generated by Django 4.0.3 on 2022-03-17 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iitle', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='')),
                ('content', models.TextField()),
                ('addedon', models.DateField(default=datetime.date(2022, 3, 17))),
            ],
        ),
        migrations.AlterField(
            model_name='registeredusers',
            name='registerDate',
            field=models.DateField(default=datetime.date(2022, 3, 17)),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='reviewDate',
            field=models.DateField(default=datetime.date(2022, 3, 17)),
        ),
    ]