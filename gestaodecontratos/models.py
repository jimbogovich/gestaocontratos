from django.db import models
import random
import string
from datetime import date, timedelta


def generate_contract_id():
    prefix = 'C'
    digits = ''.join(random.choices(string.digits, k=5))  # Ex: 12345
    return prefix + digits

STATUS = [
    ('ativo', 'Ativo'),
    ('rascunho', 'Rascunho'),
    ('encerrado', 'Encerrado'),
]

CONTRACT_TYPE_CHOICES = [
        ('manutencao', 'Manutenção'),
        ('servicos', 'Serviços'),
        ('suprimentos', 'Suprimentos'),
        ('Internet', 'Internet'),
        ('telefonia', 'Telefonia'),
        # Adicione outros tipos conforme necessário
    ]

FREQUENCY_CHOICES = [
    ('once', 'Única'),
    ('daily', 'Diária'),
    ('weekly', 'Semanal'),
    ('monthly', 'Mensal'),
]

class Clientes(models.Model):
    nome = models.CharField(max_length=250)

    def __str__(self):
        return self.nome

class TipoContratos(models.Model):
    tipos = models.CharField(choices=CONTRACT_TYPE_CHOICES, max_length=100)

    def __str__(self):
        return self.tipos


class contactManagement_db(models.Model):
    contract_id = models.CharField(max_length=10, unique=True, editable = False, verbose_name= 'Contract ID', null=True, blank=True )
    title = models.CharField(max_length=250, verbose_name='Contract Title')
    client = models.ForeignKey(Clientes, on_delete=models.PROTECT, verbose_name='Client')
    type_contract = models.CharField(choices=CONTRACT_TYPE_CHOICES, verbose_name='Contract Type', null=True, max_length=100)
    date_begin = models.DateField(null=False, verbose_name='Start Date')
    date_end = models.DateField(null=False, verbose_name='End Date')
    description = models.TextField(null=True, verbose_name='Description')
    contract_value = models.FloatField(max_length=100, null=False, blank=True, verbose_name='Contract Value')
    status = models.CharField(max_length=100, blank= False, choices=STATUS, verbose_name='Status', null=False)
    document = models.FileField(upload_to="visualizacaocontrato/", verbose_name='Document', null=True, blank=True)

    @property
    def status_label(self):
        today = date.today()
        if self.date_end < today:
            return 'Expirado'
        elif self.date_end <= today + timedelta(days=30):
            return 'Encerrando'
        else:
            return 'Ativo'
    def __str__(self):
        return f"{self.contract_id} - {self.title}"
    def save(self, *args, **kwargs):
        if not self.contract_id:
            new_id = generate_contract_id()
            while contactManagement_db.objects.filter(contract_id=new_id).exists():
                new_id = generate_contract_id()
            self.contract_id = new_id
        super().save(*args, **kwargs)

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    type = models.CharField(max_length=100, verbose_name="Tipo de Cliente", choices=[('pessoa_fisica', 'Pessoa Física'), ('pessoa_juridica', 'Pessoa Jurídica')])
    cnpjoucpf = models.CharField(max_length=18, verbose_name="CNPJ/CPF do Cliente", blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name="Email do Cliente", blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name="Telefone do Cliente", blank=True, null=True)
    address = models.CharField(max_length=100, verbose_name="Endereço do Cliente", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Cidade do Cliente", blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name="Estado do Cliente", blank=True, null=True)
    zip_code = models.CharField(max_length=8, verbose_name="CEP do Cliente", blank=True, null=True)

    def __str__(self):
        return self.name + " - " + self.email

class Reminder(models.Model):
    notify_name = models.CharField("Nome do Lembrete", max_length=255)
    reminder_type = models.CharField(choices=CONTRACT_TYPE_CHOICES,verbose_name='Tipo', null=True, blank=True, max_length=100)
    contract = models.ForeignKey(contactManagement_db, on_delete=models.SET_NULL, null=True, blank=True)
    reminder_date = models.DateField("Data do Lembrete")
    notify_days_before = models.CharField("Dias antes para notificar", max_length=2)
    frequency = models.CharField("Frequência", max_length=20, choices=FREQUENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    def __str__(self):
        return self.reminder_type








