# Generated by Django 3.2.19 on 2023-06-13 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_api', '0005_payment_requested_subscription_months'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='GBP', max_length=3),
            preserve_default=False,
        ),
    ]
