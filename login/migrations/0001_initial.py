# Generated by Django 5.1.2 on 2024-11-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=64)),
                ("hash_sha256", models.CharField(max_length=256)),
                ("is_instructor", models.BooleanField(default=False)),
            ],
        ),
    ]
