import tempfile
from typing import Any, Type

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import ModelForm
from django.http import FileResponse, Http404, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django_htmx.http import (
    HttpResponseClientRedirect,
    HttpResponseClientRefresh,
)

from edifices.forms import EdificeForm, MonthBillingForm, ResidenceForm
from edifices.models import (
    CondominiumBilling,
    Edifice,
    MonthBilling,
    Residence,
)


class DashboardView(View):
    template_name = 'dashboard.html'
    form_class = EdificeForm

    def get(self, request: HttpRequest):
        edifices = Edifice.objects.filter(user=request.user)
        form = self.form_class()
        context = {
            'edifices': edifices,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'partials/form.html', context)

        edifice = form.save(commit=False)
        edifice.user = request.user
        edifice.save()

        return HttpResponseClientRefresh()


class EdificeView(View):
    template_name = 'edifice.html'
    edit_edifice_form_class = EdificeForm
    add_residence_form_class = ResidenceForm

    form_classes_dict: dict[str, Type[ModelForm]] = {
        'edit-edifice-form': edit_edifice_form_class,
        'add-residence-form': add_residence_form_class,
    }

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            self.edifice = Edifice.objects.prefetch_related('residences').get(
                user=request.user,
                id=kwargs.get('edifice_id'),
            )
        except Edifice.DoesNotExist:
            raise Http404 from None

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, edifice_id: int):
        add_residence_form_class = self.add_residence_form_class()
        edit_edifice_form_class = self.edit_edifice_form_class(
            instance=self.edifice
        )

        condominiums = self.edifice.monthly_billings.order_by('-month')

        context = {
            'edifice': self.edifice,
            'condominiums': condominiums,
            'add_residence_form_class': add_residence_form_class,
            'edit_edifice_form_class': edit_edifice_form_class,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, edifice_id: int):
        if not (
            form_class := self.form_classes_dict.get(
                request.headers.get('form-class')
            )
        ):
            raise Http404() from None

        form = form_class(
            request.POST,
            instance=self.edifice if form_class == EdificeForm else None,
        )

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'partials/form.html', context)

        if isinstance(form, EdificeForm):
            form.save()
        if isinstance(form, ResidenceForm):
            residence = form.save(commit=False)
            residence.edifice = self.edifice
            residence.save()

        return HttpResponseClientRefresh()


@method_decorator([transaction.atomic, login_required], 'dispatch')
class GenerateCondominiumView(View):
    template_name = 'generate_condominium.html'
    form_class = MonthBillingForm

    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            self.edifice = Edifice.objects.prefetch_related('residences').get(
                user=request.user,
                id=kwargs.get('edifice_id'),
            )
        except Edifice.DoesNotExist:
            raise Http404 from None

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, edifice_id: int):
        context = {
            'edifice': self.edifice,
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, edifice_id: int):
        form = self.form_class(request.POST)
        if not form.is_valid():
            context = {'form': form, 'col_class': 'col-md-4'}
            return render(request, 'partials/form.html', context)

        month_billing: MonthBilling = form.save(commit=False)
        month_billing.edifice = self.edifice

        condominium_billings = []
        residences_to_update = []
        for residence in month_billing.edifice.residences.all():
            water_reading = request.POST.get(f'water_reading_{residence.id}')

            if not water_reading or not self.is_float(water_reading):
                form.add_error(
                    None, f'Preencha a medições do/a {residence} corretamente.'
                )

            condominium = CondominiumBilling(
                residence=residence,
                month_billing=month_billing,
                initial_water_reading=residence.last_water_reading,
                final_water_reading=water_reading,
                rent=residence.rent,
            )
            if month_billing.charge_iptu:
                condominium.iptu = residence.iptu

            condominium_billings.append(condominium)

            residence.last_water_reading = water_reading
            residences_to_update.append(residence)

        if not form.is_valid():
            context = {'form': form, 'col_class': 'col-md-4'}
            return render(request, 'partials/form.html', context)

        month_billing.save()

        CondominiumBilling.objects.bulk_create(condominium_billings)

        Residence.objects.bulk_update(
            residences_to_update,
            fields=['last_water_reading'],
        )

        messages.success(request, 'Condomínio gerado com sucesso.')
        return HttpResponseClientRedirect(
            reverse(
                'edifice',
                kwargs={'edifice_id': edifice_id},
            )
        )


class ResidenceDetailView(View):
    form_class = ResidenceForm
    template_name = 'residence_detail.html'

    def get(self, request: HttpRequest, residence_id: int):
        residence = get_object_or_404(
            Residence, id=residence_id, edifice__user=request.user
        )

        form = self.form_class(instance=residence)
        for _, field in form.fields.items():
            field.disabled = True

        context = {
            'residence': residence,
            'form': form,
        }

        return render(request, self.template_name, context)


class ResidenceUpdateView(View):
    form_class = ResidenceForm
    template_name = 'residence_update.html'

    def get(self, request: HttpRequest, residence_id: int):
        residence = get_object_or_404(
            Residence, id=residence_id, edifice__user=request.user
        )
        form = self.form_class(instance=residence)

        context = {
            'residence': residence,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, residence_id: int):
        residence = get_object_or_404(
            Residence, id=residence_id, edifice__user=request.user
        )
        form = self.form_class(request.POST, instance=residence)

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'partials/form.html', context)

        form.save()
        messages.success(request, 'Residência atualizada com sucesso.')
        return HttpResponseClientRedirect(
            reverse('residence_detail', kwargs={'residence_id': residence_id})
        )


class CondominiumView(View):
    template_name = 'condominium.html'

    def get(self, request: HttpRequest, condominium_id: int):
        condominium = get_object_or_404(
            MonthBilling, id=condominium_id, edifice__user=request.user
        )
        context = {'condominium': condominium}
        return render(request, self.template_name, context)


class CondominiumBillingPdfView(View):
    condominium_query = CondominiumBilling.objects.select_related('residence')

    def get(self, request: HttpRequest, condominium_billing_id: int):
        billing = get_object_or_404(
            self.condominium_query,
            id=condominium_billing_id,
            residence__edifice__user=request.user,
        )

        filename = (
            f'Condomínio {billing.residence} {billing.month_billing.month}.pdf'
        )

        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp_pdf:
            fields = {
                'ALUGUEL': 'rent',
                'ÁGUA': 'water_price',
                'ENERGIA': 'energy_price',
                'FAXINEIRA': 'cleaning_price',
                'MATERIAL DE LIMPEZA': 'cleaning_material_price',
                'TAXA DE LIXO': 'trash_bill_price',
                'TAXA DE ESGOTO': 'sewage_price',
                'IPTU': 'iptu',
                'TAXA FIXA': 'residence.edifice.fixed_bill',
            }
            billing.generate_pdf(fields, tmp_pdf.name)
            tmp_pdf.seek(0)
            response = FileResponse(
                open(tmp_pdf.name, 'rb'),
                content_type='application/pdf',
                filename=filename,
            )

        return response
