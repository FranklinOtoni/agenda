from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
import calendar
from calendar import HTMLCalendar

from django.views import generic

# Create your views here.

#def eventos(request, titulo_evento):
#    evento = Evento.objects.get(titulo__iexact=titulo_evento)
#    local_evento = evento.local
#    return HttpResponse('Segue o local do evento: {}'.format(local_evento))

# def index(request):
#     return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')
def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request,"Usuário ou senha inválido")
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    if year:
        current_year = int(year)
        current_month =int(month)
    else:
        now = datetime.now()
        current_year = now.year
        current_month = now.month


    n_cal = datetime(current_year,current_month,1)

    p_cal = n_cal - timedelta(days=3)

    n_cal = n_cal + timedelta(days=35)

    n_cal = 'year='+str(n_cal.year) + '&month=' + str(n_cal.month)
    p_cal = 'year='+str(p_cal.year) + '&month=' + str(p_cal.month)

#    data_atual = '01/' + str(current_month) + '/' + str(current_year)
#    data_final = data_atual + timedelta(hours=30)
    usuario = request.user
    data_atual = datetime.now() -timedelta(hours=10)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__month=current_month)

    dados = {'eventos':evento}

    #criando um calendário
    cal = HTMLCalendar().formatmonth(current_year, current_month)
    cal = cal.replace('<table border="0" cellpadding="0" cellspacing="0" class="month">','<table border="0" cellpadding="0" cellspacing="0" class="table month">')

    for x in evento:
        dt_evento = int(x.data_evento.strftime('%d'))
        dt_evento = '">' + str(dt_evento) + '<'
        alteracao = ' table-primary'+dt_evento + 'a href="evento/?id='+ str(x.id) + '"> '+ x.titulo + '</a><'
        cal=cal.replace(dt_evento, alteracao)

    dados['calendar'] = cal
    dados['pcal'] = p_cal
    dados['ncal'] = n_cal

    return render(request, 'agenda.html', dados )

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)

    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo=titulo
                evento.data_evento=data_evento
                evento.descricao=descricao
                evento.local=local
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            data_evento=data_evento,
            #                                            descricao=descricao,
            #                                            local=local
            # )
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  local=local,
                                  usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values ('id', 'titulo')
    return JsonResponse(list(evento), safe=False)

def cadastro_novo(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_repeat= request.POST.get("password_repeat")
        new_email = request.POST.get("email")
        usuario = authenticate(username=username, password=password)
        if usuario is None:
            if password==password_repeat:
                # Create user and save to the database
                user = User.objects.create_user(username, new_email, password)
                user.save()
                #login(request, usuario)
                return redirect('/')
            else:
                messages.error(request,"Senha diferente")
        else:
            login(request, usuario)
            return redirect('/')

    return redirect('/')
