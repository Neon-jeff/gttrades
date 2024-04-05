# Generated by Django 4.2.6 on 2024-04-04 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='trading_profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trading_profile', to='accounts.copytrader'),
        ),
    ]