# Generated by Django 5.1 on 2024-08-11 15:47

import django.core.validators
import django.db.models.deletion
import django.db.models.expressions
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edifices', '0002_edifice_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='edifice',
            name='fixed_bill',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='taxa fixa'),
        ),
        migrations.AlterField(
            model_name='condominiumbilling',
            name='final_water_reading',
            field=models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='medição da água final'),
        ),
        migrations.AlterField(
            model_name='condominiumbilling',
            name='initial_water_reading',
            field=models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='medição da água inicial'),
        ),
        migrations.AlterField(
            model_name='condominiumbilling',
            name='month_billing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='condominium_billings', to='edifices.monthbilling', verbose_name='cobrança mensal'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='condominiumbilling',
            name='residence',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='condominium_billings', to='edifices.residence', verbose_name='residência'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='edifice',
            name='qtd_residences',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='QTD de residências'),
        ),
        migrations.AlterField(
            model_name='edifice',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.expressions.Case, related_name='edifices', to=settings.AUTH_USER_MODEL, verbose_name='usuário'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='monthbilling',
            name='cleaning_bill_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='valor da taxa de limpeza'),
        ),
        migrations.AlterField(
            model_name='monthbilling',
            name='edifice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='monthly_billings', to='edifices.edifice', verbose_name='edifício'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='monthbilling',
            name='electricity_bill_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='valor da conta de energia'),
        ),
        migrations.AlterField(
            model_name='monthbilling',
            name='water_bill_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='valor da conta de água'),
        ),
        migrations.AlterField(
            model_name='residence',
            name='edifice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='residences', to='edifices.edifice', verbose_name='edifício'),
        ),
        migrations.AlterField(
            model_name='residence',
            name='last_water_reading',
            field=models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='última medição de água'),
        ),
    ]