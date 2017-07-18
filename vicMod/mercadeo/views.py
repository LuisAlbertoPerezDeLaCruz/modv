from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import auth
from .models import *


# Create your views here.
def login(request, method='POST'):
    disciplinas = Disciplina.objects.all()
    form = RegisterForm()
    if request.user.is_authenticated():
        actual = Dueno.objects.filter(d_user__username=request.user.username)[0]
        return redirect('/' + actual.d_marca.m_alias + "/dashboard")
    elif request.method == 'POST':
        if request.POST['form-type'] == u"registro":
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                return render(request, "index.html", {'next': 'index', 'disciplinas': disciplinas, })
            else:
                mensaje = "Forma no valida"
                marcas_publicas = Marca.objects.filter(m_public=True).order_by('m_nombre')[0:5]
                return render(request, "index.html", {'next': 'index', 'disciplinas': disciplinas, 'mensaje': mensaje,
                                                      'marcas_publicas': marcas_publicas, })
        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                perfil = UserProfile.objects.get(u_user=request.user)
                if perfil.u_marca:
                    actual = Dueno.objects.filter(d_user__username=username)[0]
                    return redirect('/' + actual.d_marca.m_alias + "/dashboard")
                else:
                    return redirect("/" + perfil.u_alias + "/dashboard")
            else:
                mensaje = ""
                marcas_publicas = Marca.objects.filter(m_public=True).order_by('m_nombre')[0:5]
                return render(request, "index.html", {'next': 'index', 'disciplinas': disciplinas, 'mensaje': mensaje,
                                                      'marcas_publicas': marcas_publicas, 'notificacion': -100})
    else:
        mensaje = ""
        marcas_publicas = Marca.objects.filter(m_public=True).order_by('m_nombre')[0:5]
        return render(request, "index.html", {'next': 'index', 'disciplinas': disciplinas, 'mensaje': mensaje,
                                              'marcas_publicas': marcas_publicas, 'notificacion': 0})


def centros(request):
    try:
        municipio = request.GET['municipio']
        m = Zona.objects.get(z_municipio=municipio)
        centros = Marca.objects.filter(m_public=True, m_municipio=m).order_by('m_nombre')
        ciudadp = m.z_ciudad.c_nombre
        municipios = Zona.objects.filter(z_ciudad=m.z_ciudad)
    except:
        municipio = "MUNICIPIO"
        try:
            ciudadp = request.GET['ciudad']
            c = Ciudad.objects.get(c_nombre=ciudadp)
            centros = Marca.objects.filter(m_public=True, m_ciudad=c).order_by('m_nombre')
            municipios = Zona.objects.filter(z_ciudad=ciudadp)
        except:
            ciudadp = "CIUDAD"
            municipios = []
            centros = Marca.objects.filter(m_public=True).order_by('m_nombre')
    ciudades = Ciudad.objects.all()
    disciplinas = Disciplina.objects.all()
    marcas_publicas = Marca.objects.filter(m_public=True).order_by('m_nombre')
    return render(request, 'centros.html', {
        'ciudades': ciudades,
        'disciplinas': disciplinas,
        'ciudadp': ciudadp,
        'municipios': municipios,
        'municipio': municipio,
        'marcas_publicas': marcas_publicas,
        'centros': centros})


def instructores(request):
    return render(request, 'instructores.html', {})


def acerca_de(request):
    return render(request, 'index.html', {})
