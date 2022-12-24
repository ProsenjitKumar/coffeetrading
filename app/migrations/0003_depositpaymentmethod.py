# Generated by Django 4.1.4 on 2022-12-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositPaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(blank=True, max_length=255)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='currency/logo/')),
                ('currency_address', models.CharField(blank=True, max_length=455, null=True)),
                ('qr_code_image', models.ImageField(blank=True, null=True, upload_to='currency/qrcode/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
    ]
