# Generated by Django 4.2.6 on 2024-04-04 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_profile_verification_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
    ]