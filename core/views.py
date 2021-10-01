from django.shortcuts import render, HttpResponse
from core.models import Evento
# Create your views here.

def eventos(request, titulo_evento):
    evento = Evento.objects.get(titulo__iexact=titulo_evento)
    local_evento = evento.local
    return HttpResponse('Segue o local do evento: {}'.format(local_evento))
