# Generated by Django 5.2 on 2025-05-29 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inkludechit', '0012_rename_first_name_salepunchmodel_full_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salepunchmodel',
            name='customer_prof',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_inkludechit.customerprofilemodel'),
        ),
    ]
