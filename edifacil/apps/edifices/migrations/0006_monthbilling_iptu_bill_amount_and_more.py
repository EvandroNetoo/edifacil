# Generated by Django 5.1 on 2024-08-11 21:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edifices', '0005_monthbilling_trash_bill_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthbilling',
            name='iptu_bill_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='valor da taxa de IPTU'),
        ),
        migrations.AddField(
            model_name='monthbilling',
            name='others_bill_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='valor da taxa de outraos'),
        ),
        migrations.AlterField(
            model_name='monthbilling',
            name='cleaning_bill_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='valor da taxa de limpeza'),
        ),
        migrations.AlterField(
            model_name='monthbilling',
            name='cleaning_material_bill_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='valor da taxa de material de limpeza'),
        ),
        migrations.AlterField(
            model_name='monthbilling',
            name='trash_bill_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='valor da taxa de lixo'),
        ),
    ]
