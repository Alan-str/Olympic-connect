# Generated by Django 5.0.6 on 2024-05-30 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('price_solo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_duo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_family', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thumbnail', models.ImageField(upload_to='events/thumbnails/')),
                ('banner', models.ImageField(upload_to='events/banners/')),
            ],
        ),
    ]
