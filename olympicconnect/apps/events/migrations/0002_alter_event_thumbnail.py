# Generated by Django 5.0.6 on 2024-05-30 23:19

import apps.events.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='thumbnail',
            field=models.ImageField(upload_to=apps.events.models.upload_to),
        ),
    ]
