# Generated by Django 3.2.23 on 2023-12-06 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='additional_field',
            field=models.CharField(default=None, max_length=255),
        ),
    ]