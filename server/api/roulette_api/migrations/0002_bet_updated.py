# Generated by Django 5.0.3 on 2024-03-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roulette_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]