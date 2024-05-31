# Generated by Django 5.0.6 on 2024-05-31 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('events', '0002_alter_event_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_at',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='offer_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='events.event'),
        ),
    ]