# Generated by Django 4.2.10 on 2024-02-24 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_delete_appuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicdetails',
            old_name='user_name',
            new_name='user',
        ),
    ]
