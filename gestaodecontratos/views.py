from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ContratosForm, ReminderForm, ClientForm, CustomUserCreationForm, DocumentoForm
from .models import contactManagement_db, Reminder, Client, Documento
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.views import LoginView


@login_required
def contratos_view(request, contract_id=None):
    contrato = None
    if contract_id:
        contrato = get_object_or_404(contactManagement_db, contract_id=contract_id)

    if request.method == 'POST':
        form = ContratosForm(request.POST, request.FILES, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect('visualizacaocontrato', contrato_id=form.instance.id)
    else:
        form = ContratosForm(instance=contrato)

    return render(request, 'contratos.html', {'form': form})

@login_required
def listagemContratos(request):
    contratos = contactManagement_db.objects.select_related('client').order_by('date_begin')

    return render(request, 'listacontratos.html', {'contratos': contratos})

@login_required
def detalhes_contrato(request, contrato_id):
    contrato = get_object_or_404(contactManagement_db, id=contrato_id)
    documentos = contrato.documentos.all()

    if request.method == 'POST':
        # Upload direto no campo principal `document`
        if request.FILES.get('document'):
            contrato.document = request.FILES['document']
            contrato.save()
            return redirect('visualizacaocontrato', contrato_id=contrato_id)

        # Upload de documentos relacionados
        if 'upload_documento' in request.POST:
            form_doc = DocumentoForm(request.POST, request.FILES)
            if form_doc.is_valid():
                doc = form_doc.save(commit=False)
                doc.contrato = contrato
                doc.save()
                return redirect('visualizacaocontrato', contrato_id=contrato_id)
    else:
        form_doc = DocumentoForm()

    return render(request, 'detalhescontrato.html', {
        'contrato': contrato,
        'documentos': documentos,
        'form_doc': form_doc
    })


@login_required
def dashboardView(request):
    today = date.today()
    total_contratos = contactManagement_db.objects.count()
    expirando = contactManagement_db.objects.filter(date_end__lte=today + timedelta(days=30),
                                                    date_end__gte=today).count()
    ativos = contactManagement_db.objects.filter(date_end__gt=today + timedelta(days=30)).count()
    contratos = contactManagement_db.objects.all()

    reminders = Reminder.objects.filter(reminder_date__gte=today).order_by('reminder_date')[:5]

    reminders_unread = Reminder.objects.filter(
        reminder_date__gte=today,
        visualizado=False
    ).order_by('reminder_date')

    return render(request, 'dashboard.html', {
        'reminders_unread': reminders_unread,
        'reminders': reminders,
        'total_contratos': total_contratos,
        'expirando': expirando,
        'ativos': ativos,
        'contratos': contratos,
    })

@login_required
def search_contracts(request):
    contratos = contactManagement_db.objects.all()

    if request.method == 'POST':
        termo = request.POST.get('busca', '').strip().lower()

        if termo:
            contratos = []
            for contrato in contactManagement_db.objects.all():
                if (
                    termo in contrato.title.lower() or
                    termo in contrato.client.nome.lower() or
                    termo in contrato.status.lower() or
                    (contrato.type_contract and termo in contrato.type_contract.tipos.lower())
                ):
                    contratos.append(contrato)
    return render(request, 'buscacontratos.html', {
        'contratos': contratos
    })

@login_required
def NotificationView(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ReminderForm()
        return render(request, 'notificacoes.html', {'form': form})

@login_required
def notificacoes_nao_lidas_api(request):
    lembretes = Reminder.objects.filter(visualizado=False).order_by('-reminder_date')[:5]
    data = {
        "notificacoes": [
            {
                "id": lembrete.id,
                "notify_name": lembrete.notify_name,
                "contract_id": lembrete.contract.id if lembrete.contract else None,
                "contract_title": lembrete.contract.title if lembrete.contract else "Sem contrato",
                "reminder_date": lembrete.reminder_date.strftime('%d/%m/%Y')
            }
            for lembrete in lembretes
        ]
    }
    return JsonResponse(data)

@login_required
def CadastroCliente(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            print('parou aqui!')

            return redirect('dashboard')
        else:
            messages.error(request, form.errors)



    form = ClientForm(request.POST or None)
    return render(request, 'cadastroclientes.html', {'form': form})

@login_required
def clientes(request):
    clientes = Client.objects.all()
    return render(request, 'listarclientes.html', {'clientes': clientes})

class CustomLoginView(LoginView):
    template_name = 'login.html'

def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def campo_cliente(request):
    return render(request, 'cliente.html')


def download_arquivo(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)

    response = FileResponse(documento.arquivo.open('rb'), as_attachment=True,
                filename=documento.arquivo.name.split('/')[-1])
    return response

def excluir_documento(request, doc_id):
    documento = get_object_or_404(Documento, id=doc_id)
    contrato_id = documento.contrato.id  # para redirecionar de volta ao contrato correto
    documento.delete()
    return redirect('visualizacaocontrato', contrato_id=contrato_id)
