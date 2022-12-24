# Generated by Django 4.1.4 on 2022-12-23 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_depositconfirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('currency_selected', models.CharField(blank=True, choices=[('1', 'Bitcoin'), ('2', 'Litecoin'), ('3', 'Ethereum')], max_length=25, null=True)),
                ('currency_address', models.CharField(blank=True, max_length=455, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('investor_user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
