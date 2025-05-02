from decimal import Decimal

import pdfkit
from accounts.models import User
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

positive_value_validator = MinValueValidator(0.01)


class Edifice(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.Case,
        related_name='edifices',
        verbose_name='usuário',
    )
    name = models.CharField('nome', max_length=255)

    fixed_bill = models.DecimalField(
        'taxa fixa',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal(0),
    )

    residences: models.QuerySet['Residence']
    monthly_billings: models.QuerySet['MonthBilling']

    class Meta:
        verbose_name = 'edifício'
        verbose_name_plural = 'edifícios'

    def __str__(self) -> str:
        return self.name

    @property
    def qtd_residences(self):
        return self.residences.all().count()


class Residence(models.Model):
    edifice = models.ForeignKey(
        Edifice,
        models.CASCADE,
        related_name='residences',
        verbose_name='edifício',
    )
    last_water_reading = models.DecimalField(
        'última medição de água',
        max_digits=10,
        decimal_places=3,
        validators=[positive_value_validator],
    )
    number = models.IntegerField('número')
    prefix = models.CharField('prefixo', max_length=20, blank=True)
    suffix = models.CharField('sufixo', max_length=20, blank=True)
    rent = models.DecimalField(
        'valor do aluguel',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal(0),
    )
    iptu = models.DecimalField(
        'valor do IPTU',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal(0),
    )

    class Meta:
        verbose_name = 'residência'
        verbose_name_plural = 'residências'

    def __str__(self) -> str:
        return f'{self.prefix} {self.number} {self.suffix}'


class MonthBilling(models.Model):
    edifice = models.ForeignKey(
        Edifice,
        models.CASCADE,
        related_name='monthly_billings',
        verbose_name='edifício',
    )
    month = models.DateField('mês', default=timezone.now)
    electricity_bill_amount = models.DecimalField(
        'valor da conta de energia',
        max_digits=10,
        decimal_places=2,
        validators=[positive_value_validator],
    )
    water_bill_amount = models.DecimalField(
        'valor da conta de água',
        max_digits=10,
        decimal_places=2,
        validators=[positive_value_validator],
    )
    cleaning_bill_amount = models.DecimalField(
        'valor da taxa de limpeza',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    cleaning_material_bill_amount = models.DecimalField(
        'valor da taxa de material de limpeza',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    trash_bill_amount = models.DecimalField(
        'valor da taxa de lixo',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    sewage_bill_amount = models.DecimalField(
        'valor da taxa de esgoto',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    charge_iptu = models.BooleanField(
        'cobrar IPTU?',
        default=False,
        help_text='Marque se deseja cobrar o IPTU do morador',
    )
    others_bill_amount = models.DecimalField(
        'valor da taxa de outros',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    condominium_billings: models.QuerySet['CondominiumBilling']

    class Meta:
        verbose_name = 'cobrança mensal'
        verbose_name_plural = 'cobranças mensais'

    def __str__(self) -> str:
        return f'{self.edifice} {self.month}'

    @property
    def qtd_residences(self):
        return self.condominium_billings.all().count()

    @property
    def water_value_by_cubic_m(self):
        water_consumes = [
            condominium_billings.water_consume
            for condominium_billings in self.condominium_billings.all()
        ]
        total_consume = sum(water_consumes)
        return self.water_bill_amount / total_consume


class CondominiumBilling(models.Model):
    residence = models.ForeignKey(
        Residence,
        models.CASCADE,
        related_name='condominium_billings',
        verbose_name='residência',
    )
    month_billing = models.ForeignKey(
        MonthBilling,
        models.CASCADE,
        related_name='condominium_billings',
        verbose_name='cobrança mensal',
    )
    initial_water_reading = models.DecimalField(
        'medição da água inicial',
        max_digits=10,
        decimal_places=3,
        validators=[positive_value_validator],
    )
    final_water_reading = models.DecimalField(
        'medição da água final',
        max_digits=10,
        decimal_places=3,
        validators=[positive_value_validator],
    )
    rent = models.DecimalField(
        'valor do aluguel',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal(0),
    )
    iptu = models.DecimalField(
        'valor do IPTU',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal(0),
    )

    class Meta:
        verbose_name = 'cobrança de condomínio'
        verbose_name_plural = 'cobranças de condomínio'

    def __str__(self) -> str:
        return f'{self.residence} {self.month_billing}'

    @property
    def water_consume(self):
        return self.final_water_reading - self.initial_water_reading

    @property
    def water_price(self):
        return self.month_billing.water_value_by_cubic_m * self.water_consume

    @property
    def energy_price(self):
        return (
            self.month_billing.electricity_bill_amount
            / self.month_billing.qtd_residences
        )

    @property
    def cleaning_price(self):
        return (
            self.month_billing.cleaning_bill_amount
            / self.month_billing.qtd_residences
        )

    @property
    def cleaning_material_price(self):
        return (
            self.month_billing.cleaning_material_bill_amount
            / self.month_billing.qtd_residences
        )

    @property
    def trash_bill_price(self):
        return (
            self.month_billing.trash_bill_amount
            / self.month_billing.qtd_residences
        )

    @property
    def sewage_price(self):
        return (
            self.month_billing.sewage_bill_amount
            / self.month_billing.qtd_residences
        )

    def generate_pdf(self, fields: dict[str, str], file: str) -> bytes:
        def get_nested_attr(obj, attr_path):
            for attr in attr_path.split('.'):
                obj = getattr(obj, attr)
            return obj

        template_name = 'partials/condominium_billing_pdf.html'

        bills = {}
        total = 0
        for verbose_name, nested_field in fields.items():
            field = get_nested_attr(self, nested_field)
            if field != 0:
                bills[verbose_name] = f'{field:.2f}'.replace('.', ',')
                total += field

        context = {
            'billing': self,
            'bills': bills,
            'total': f'{total:.2f}'.replace('.', ','),
        }
        html = render_to_string(template_name, context)
        pdfkit.from_string(html, file, options=settings.PDFKIT_OPTIONS)
