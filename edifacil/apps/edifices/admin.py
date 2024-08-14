from django.contrib import admin

from edifices.models import (
    CondominiumBilling,
    Edifice,
    MonthBilling,
    Residence,
)

admin.site.register(Edifice)
admin.site.register(Residence)
admin.site.register(MonthBilling)
admin.site.register(CondominiumBilling)
