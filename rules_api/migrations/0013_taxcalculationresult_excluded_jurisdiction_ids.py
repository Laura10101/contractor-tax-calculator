# Generated by Django 3.2.19 on 2024-02-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_api', '0012_alter_secondarytieredraterule_primary_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxcalculationresult',
            name='excluded_jurisdiction_ids',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]