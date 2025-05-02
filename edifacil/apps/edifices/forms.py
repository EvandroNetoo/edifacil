from datetime import datetime

from django import forms

from edifices.models import (
    Edifice,
    MonthBilling,
    Residence,
)


class EdificeForm(forms.ModelForm):
    class Meta:
        model = Edifice
        fields = ['name', 'fixed_bill']


class ResidenceForm(forms.ModelForm):
    class Meta:
        model = Residence
        fields = [
            'last_water_reading',
            'number',
            'prefix',
            'suffix',
            'rent',
            'iptu',
        ]


class MonthField(forms.DateField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            # Converte "YYYY-MM" para o primeiro dia do mês correspondente
            return datetime.strptime(value, '%Y-%m').date().replace(day=1)
        except (ValueError, TypeError):
            raise forms.ValidationError(
                "Formato de mês inválido. Utilize 'YYYY-MM'."
            ) from None


class MonthBillingForm(forms.ModelForm):
    month = MonthField(widget=forms.DateInput(attrs={'type': 'month'}))

    class Meta:
        model = MonthBilling
        fields = [
            'month',
            'electricity_bill_amount',
            'water_bill_amount',
            'cleaning_bill_amount',
            'cleaning_material_bill_amount',
            'trash_bill_amount',
            'sewage_bill_amount',
            'others_bill_amount',
            'charge_iptu',
        ]
