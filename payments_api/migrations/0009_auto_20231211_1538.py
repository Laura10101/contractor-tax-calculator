# Generated by Django 3.2.19 on 2023-12-11 15:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_api', '0008_auto_20230618_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='subscription_option_id',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='total',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
