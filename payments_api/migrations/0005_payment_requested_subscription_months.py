# Generated by Django 3.2.19 on 2023-06-13 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_api', '0004_auto_20230613_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='requested_subscription_months',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]
