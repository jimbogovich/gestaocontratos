from django.contrib import admin
from django.urls import path, include
from .views import contratos_view, listagemContratos, detalhes_contrato, dashboardView, search_contracts, NotificationView

urlpatterns = [
    path('gestaodecontratos/', contratos_view, name='gestaodecontratos'),
    path('listadecontratos/', listagemContratos, name='listadecontratos' ),
    path('contrato/<int:contrato_id>/', detalhes_contrato, name='visualizacaocontrato'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('buscacontrato/', search_contracts, name='buscacontrato'),
    path('notificacoes/', NotificationView, name='notificacoes')
]