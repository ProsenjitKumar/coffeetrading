# Generated by Django 4.1.4 on 2022-12-22 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_depositpaymentmethod'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_deposited', models.FloatField()),
                ('currency_selected', models.CharField(blank=True, choices=[('1', 'Bitcoin'), ('2', 'Litecoin'), ('3', 'Ethereum')], max_length=25, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=450, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('investor_user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_confirmation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
