from django.urls import path
from .views import contratos_view, listagemContratos, detalhes_contrato, dashboardView, search_contracts, NotificationView, notificacoes_nao_lidas_api, CadastroCliente, clientes, login, logout

urlpatterns = [
    path('gestaodecontratos/', contratos_view, name='gestaodecontratos'),
    path('listadecontratos/', listagemContratos, name='listadecontratos' ),
    path('contrato/<int:contrato_id>/', detalhes_contrato, name='visualizacaocontrato'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('buscacontrato/', search_contracts, name='buscacontrato'),
    path('notificacoes/', NotificationView, name='notificacoes'),
    path('api/notificacoes_nao_lidas/', notificacoes_nao_lidas_api, name='notificacoes_nao_lidas_api'),
    path('cadastroclientes/', CadastroCliente, name='cadastroclientes'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]