# Generated by Django 3.2.19 on 2024-01-16 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rules_api', '0011_auto_20240116_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondarytieredraterule',
            name='primary_rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='secondary_rules', to='rules_api.tieredraterule'),
        ),
    ]
