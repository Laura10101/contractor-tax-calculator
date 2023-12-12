# Generated by Django 3.2.19 on 2023-12-12 16:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_api', '0004_auto_20231212_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruletier',
            name='tier_rate',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='secondaryruletier',
            name='tier_rate',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]