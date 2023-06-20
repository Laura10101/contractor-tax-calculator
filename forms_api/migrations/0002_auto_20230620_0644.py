# Generated by Django 3.2.19 on 2023-06-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='numericquestion',
            name='validation_rule',
        ),
        migrations.AddField(
            model_name='numericquestion',
            name='is_integer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='numericquestion',
            name='max_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='numericquestion',
            name='min_value',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='NumericAnswerValidationRule',
        ),
    ]
