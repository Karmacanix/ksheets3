# Generated by Django 5.1.2 on 2024-10-16 15:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BusinessUnit",
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
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "name",
                    models.CharField(max_length=254, primary_key=True, serialize=False),
                ),
                (
                    "project_status",
                    models.CharField(
                        choices=[
                            ("N", "New"),
                            ("W", "In Progress"),
                            ("H", "On Hold"),
                            ("C", "Closed"),
                        ],
                        default="N",
                        max_length=1,
                        verbose_name="Status",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("businessunit", models.ManyToManyField(to="project.businessunit")),
                (
                    "projectmanager",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projectmanager",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
