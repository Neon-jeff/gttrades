# Generated by Django 4.2.6 on 2024-04-05 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_copyexpertrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='expert_trade',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='trade',
            name='lost_trade',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
