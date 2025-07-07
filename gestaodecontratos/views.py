from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ContratosForm, ReminderForm
from .models import contactManagement_db, Reminder
from datetime import date, timedelta

def contratos_view(request):
    if request.method == 'POST':
        form = ContratosForm(request.POST)

        if form.is_valid():
           form.save()
           messages.success(request, "Contrato saved suceffully")
        else:
            messages.error(request, form.errors)


    form = ContratosForm()
    return render(request, 'contratos.html', {'form': form })

def listagemContratos(request):
    contratos = contactManagement_db.objects.select_related('client').order_by('date_begin')

    return render(request, 'listacontratos.html', {'contratos': contratos})

def detalhes_contrato(request, contrato_id):
    contrato = get_object_or_404(contactManagement_db, id=contrato_id)

    if request.method == 'POST' and request.FILES.get('document'):
        contrato.document = request.FILES['document']
        contrato.save()

    return render(request, 'detalhescontrato.html', {'contrato': contrato})

def dashboardView(request):
    today = date.today()
    total_contratos = contactManagement_db.objects.count()
    expirando = contactManagement_db.objects.filter(date_end__lte=today + timedelta(days=30),
                                                    date_end__gte=today).count()
    ativos = contactManagement_db.objects.filter(date_end__gt=today + timedelta(days=30)).count()
    contratos = contactManagement_db.objects.all()


    return render(request, 'dashboard.html', {
        'total_contratos': total_contratos,
        'expirando': expirando,
        'ativos': ativos,
        'contratos': contratos,
    })

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

def NotificationView(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = ReminderForm()
        return render(request, 'notificacoes.html', {'form': form})
















