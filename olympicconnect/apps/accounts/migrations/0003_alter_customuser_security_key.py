# Generated by Django 5.0.6 on 2024-06-02 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_security_key_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='security_key',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
