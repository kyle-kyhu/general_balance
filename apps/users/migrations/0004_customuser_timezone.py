# Generated by Django 5.0.4 on 2024-05-17 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_auto_20240516_1952"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="timezone",
            field=models.CharField(default="UTC", max_length=100),
        ),
    ]
