from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('gestaodecontratos/', views.contratos_view, name='gestaodecontratos'),
    path('documento/<int:documento_id>/download/', views.download_arquivo, name='download_arquivo'),
    path('documento/<int:doc_id>/excluir/', views.excluir_documento, name='excluir_documento'),
    path('gestaodecontratos/<str:contract_id>/', views.contratos_view, name='editar_contrato'),
    path('listadecontratos/', views.listagemContratos, name='listadecontratos' ),
    path('contrato/<int:contrato_id>/', views.detalhes_contrato, name='visualizacaocontrato'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('buscacontrato/', views.search_contracts, name='buscacontrato'),
    path('notificacoes/', views.NotificationView, name='notificacoes'),
    path('api/notificacoes_nao_lidas/', views.notificacoes_nao_lidas_api, name='notificacoes_nao_lidas_api'),
    path('cadastroclientes/', views.CadastroCliente, name='cadastroclientes'),
    path('clientes/', views.clientes, name='clientes'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dadoscliente/', views.campo_cliente, name='dadoscliente')
]

