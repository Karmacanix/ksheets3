# Generated by Django 5.1.2 on 2024-10-21 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='customer.customer'),
            preserve_default=False,
        ),
    ]
