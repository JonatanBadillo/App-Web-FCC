# Generated by Django 5.0.2 on 2024-02-26 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("computacion_api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Administradores",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "clave_admin",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("telefono", models.CharField(blank=True, max_length=255, null=True)),
                ("rfc", models.CharField(blank=True, max_length=255, null=True)),
                ("edad", models.IntegerField(blank=True, null=True)),
                ("ocupacion", models.CharField(blank=True, max_length=255, null=True)),
                ("creation", models.DateTimeField(auto_now_add=True, null=True)),
                ("update", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Profiles",
        ),
    ]
