# Generated by Django 5.2 on 2025-05-25 17:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inkludechit', '0004_alter_customerprofilemodel_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofilemodel',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
    ]
