# Generated by Django 5.0.6 on 2024-06-01 01:21

import apps.users.helpers
import apps.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.FileField(blank=True, upload_to=apps.users.models._get_avatar_filename, validators=[apps.users.helpers.validate_profile_picture]),
        ),
    ]
