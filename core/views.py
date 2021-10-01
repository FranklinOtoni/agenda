from django.shortcuts import render, redirect, HttpResponse
from core.models import Evento
# Create your views here.

def eventos(request, titulo_evento):
    evento = Evento.objects.get(titulo__iexact=titulo_evento)
    local_evento = evento.local
    return HttpResponse('Segue o local do evento: {}'.format(local_evento))

# def index(request):
#     return redirect('/agenda/')

def lista_eventos(request):
    #usuario = request.user
    #evento = Evento.objects.filter(usuario=usuario)
    evento = Evento.objects.all()
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)
