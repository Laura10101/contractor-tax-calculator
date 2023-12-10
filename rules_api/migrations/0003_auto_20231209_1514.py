# Generated by Django 3.2.19 on 2023-12-09 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rules_api', '0002_rule_ruleset'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxCalculationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaxRuleSetResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jurisdiction_id', models.IntegerField()),
                ('tax_category_id', models.IntegerField()),
                ('tax_category_name', models.CharField(max_length=255)),
                ('ordinal', models.IntegerField()),
                ('tax_calculation_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='rules_api.taxcalculationresult')),
            ],
        ),
        migrations.AddField(
            model_name='ruleset',
            name='ordinal',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rule',
            name='ruleset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='rules_api.ruleset'),
        ),
        migrations.AlterField(
            model_name='ruletier',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tiers', to='rules_api.tieredraterule'),
        ),
        migrations.AlterField(
            model_name='secondaryruletier',
            name='primary_tier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='rules_api.ruletier'),
        ),
        migrations.AlterField(
            model_name='secondaryruletier',
            name='secondary_rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tiers', to='rules_api.secondarytieredraterule'),
        ),
        migrations.CreateModel(
            name='TaxRuleTierResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_id', models.IntegerField()),
                ('rule_model_name', models.CharField(max_length=255)),
                ('rule_name', models.CharField(max_length=255)),
                ('tier_id', models.IntegerField(null=True)),
                ('tier_model_name', models.CharField(max_length=255, null=True)),
                ('tier_name', models.CharField(max_length=255, null=True)),
                ('variable_name', models.CharField(max_length=255)),
                ('variable_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('taxable_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=4)),
                ('tax_payable', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ordinal', models.IntegerField()),
                ('ruleset_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='rules_api.taxrulesetresult')),
            ],
        ),
    ]