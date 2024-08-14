from django.urls import path

from edifices import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path(
        'edifice/<int:edifice_id>/',
        views.EdificeView.as_view(),
        name='edifice',
    ),
    path(
        'edifice/<int:edifice_id>/generate_condominium',
        views.GenerateCondominiumView.as_view(),
        name='generate_condominium',
    ),
    path(
        'condominium/<int:condominium_id>',
        views.CondominiumView.as_view(),
        name='condominium',
    ),
    path(
        'condominium_billing_pdf/<int:condominium_billing_id>',
        views.CondominiumBillingPdfView.as_view(),
        name='condominium_billing_pdf',
    ),
]
