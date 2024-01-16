# Generated by Django 3.2.19 on 2024-01-16 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rules_api', '0008_secondaryruletier_ordinal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondaryruletier',
            name='primary_tier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='rules_api.ruletier'),
        ),
        migrations.AlterField(
            model_name='secondarytieredraterule',
            name='primary_rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rules_api.tieredraterule'),
        ),
    ]
