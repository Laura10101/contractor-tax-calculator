# Generated by Django 3.2.19 on 2024-01-16 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules_api', '0010_auto_20240116_1054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rule',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelManagers(
            name='flatraterule',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='rule',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='secondarytieredraterule',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='tieredraterule',
            managers=[
            ],
        ),
    ]