# Generated by Django 4.1.4 on 2022-12-23 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_withdrawalrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawalrequest',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=200, unique=True),
        ),
    ]
