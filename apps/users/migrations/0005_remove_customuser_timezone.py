# Generated by Django 5.0.4 on 2024-05-17 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_customuser_timezone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="timezone",
        ),
    ]
