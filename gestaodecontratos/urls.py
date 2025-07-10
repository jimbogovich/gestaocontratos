from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('gestaodecontratos/', views.contratos_view, name='gestaodecontratos'),
    path('listadecontratos/', views.listagemContratos, name='listadecontratos' ),
    path('contrato/<int:contrato_id>/', views.detalhes_contrato, name='visualizacaocontrato'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('buscacontrato/', views.search_contracts, name='buscacontrato'),
    path('notificacoes/', views.NotificationView, name='notificacoes'),
    path('api/notificacoes_nao_lidas/', views.notificacoes_nao_lidas_api, name='notificacoes_nao_lidas_api'),
    path('cadastroclientes/', views.CadastroCliente, name='cadastroclientes'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
]