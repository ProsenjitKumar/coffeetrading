# Generated by Django 4.1.4 on 2022-12-23 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_withdrawalrequest_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
    ]
