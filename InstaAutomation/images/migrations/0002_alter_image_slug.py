# Generated by Django 5.0.6 on 2024-12-03 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]