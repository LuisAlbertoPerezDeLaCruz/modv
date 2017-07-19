from django.shortcuts import render
from ..mercadeo.models import *
from ..manejoCalendario.models import *
from .models import *
from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models import Sum

def getnotificacionesmarca(marca,n):
	notificaciones = []
	notificaciones.append(Notificacion.objects.filter(n_marca = marca,n_tipo = "R").order_by('-n_fecha')[0:n])
	notificaciones.append(Notificacion.objects.filter(n_marca=marca,n_tipo="E").order_by('-n_fecha')[0:n])
	notificaciones.append(Notificacion.objects.filter(n_marca=marca,n_tipo__in=["A","P","C"]).order_by('-n_fecha')[0:n])
	notificaciones.append(Notificacion.objects.filter(n_marca=marca,n_tipo='S').order_by('-n_fecha')[0:n])
	notificaciones.append(len(notificaciones[0]) + len(notificaciones[1]) + len(notificaciones[2]))
	notificaciones.append(len(notificaciones[3]))
	return notificaciones

def getnotificacionesusuario(user,n):
	notificaciones = []
	notificaciones.append(Notificacion.objects.filter(n_notificador = user,n_tipo = "R").order_by('-n_fecha')[0:n])
	notificaciones.append(Notificacion.objects.filter(n_notificador = user,n_tipo="E").order_by('-n_fecha')[0:n])
	notificaciones.append(Notificacion.objects.filter(n_notificador = user,n_tipo__in=["A","P","C"]).order_by('-n_fecha')[0:n])
	notificaciones.append(Notificacion.objects.filter(n_notificador = user,n_tipo='S').order_by('-n_fecha')[0:n])
	notificaciones.append(len(notificaciones[0]) + len(notificaciones[1]) + len(notificaciones[2]))
	notificaciones.append(len(notificaciones[3]))
	return notificaciones

def getmes(i):
	meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
	return meses[i]

def dashboard(request,pk):
	try:
		hoy = datetime.strptime(request.GET['fecha'],'%Y-%m-%d')
	except:
		hoy = datetime.today()
	relacion = Relacion.objects.values_list('r_marca',flat=True).filter(r_estado="A",r_user=request.user)
	mare = Marca.objects.filter(pk__in=relacion)
	marcas_publicas = Marca.objects.filter(m_public=True).order_by('m_nombre') | mare
	try:
		notificacion = request.GET['notificacion']
	except:
		notificacion = 0
	perfil = UserProfile.objects.get(u_user=request.user)
	hoy = hoy.replace(hour=0,minute=0,second=0)
	pasada = hoy - timedelta(days=7)
	dia_hoy = hoy.day
	dia_sem = hoy.weekday()
	ini_sem = (hoy - timedelta(days= hoy.weekday()))
	fin_sem = ini_sem + timedelta(days=7)
	sem = []
	sem_date = []
	for x in range (0, 8):
		sem.append((ini_sem + timedelta(days = x)).day)
		sem_date.append(ini_sem + timedelta(days = x))
	pasado = []
	for x in sem_date:
		pasado.append(x < datetime.today())
	print(pasado)

	if perfil.u_marca :
		marcas = Dueno.objects.filter(d_user=request.user)
		actual = Marca.objects.get(m_alias=pk)
		actividades_semana = []
		confirmados_semana = []
		reservas_semana = []
		enespera_semana = []
		cuposenespera_semana = []
		cuentas = []
		disciplinas = Disciplina.objects.all()
		ids = Relacion.objects.values_list('r_user__pk',flat=True).filter(r_marca=actual,r_entrenador=True)
		instructores = User.objects.filter(pk__in=set(ids))
		salones = Salon.objects.filter(s_marca=actual)
		for i in range(0, 8):
			actividades = Actividad.objects.filter(ac_marca = actual,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).order_by('ac_hora_ini')
			series = []
			cuentas.append(actividades.count())
			for a in actividades:
				if Serie.objects.filter(s_actividad=a).exists() :
					series.append([int(Serie.objects.get(s_actividad = a).s_num_ser),a.pk])
				else:
					series.append([0,0])
			actividades_semana.append(zip(actividades,series))
			confirmados_semana.append(Actividad.objects.filter(ac_marca = actual,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cupos_reservados'),0)))
			reservas_semana.append(Actividad.objects.filter(ac_marca = actual,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cap_max'),0)))
			if not pasado[i]:
				enespera_semana.append(Actividad.objects.filter(ac_marca = actual,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cupos_en_espera'),0)))
				cuposenespera_semana.append(Actividad.objects.filter(ac_marca = actual,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cap_max_espera'),0)))
			else:
				lista = actividades.values_list('pk',flat=True)
				participantes = Participantes.objects.filter(pa_actividad__in=lista,pa_asistencia=True).count()
				enespera_semana.append(participantes)
				cuposenespera_semana.append(Actividad.objects.filter(ac_marca = actual,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cupos_reservados'),0)))
		maximo = max(cuentas)
		print(cuentas)
		print(maximo)
		minimo = list(map((lambda x: range(maximo-x) ), cuentas))
		print(minimo)
		return render(request, 'entrenador-calendario.html', {
			'dia_hoy':str(dia_hoy),
			'ini_sem':str(ini_sem.day),
			'inicio_sem':ini_sem,
			'pasada':pasada,
			'fin_de_sem':fin_sem,
			'fin_sem':str(fin_sem.day),
			'dia_sem':dia_sem,
			'sem':sem,
			'pk':pk,
			'mes':getmes(ini_sem.month-1),
			'maximo':maximo,
			'perfil':perfil,
			'minimo':minimo,
			'pasado':pasado,
			'marcas_publicas':marcas_publicas,
			'sem_date':sem_date,
			'notificaciones':getnotificacionesmarca(actual,25),
			'hoy':hoy,
			'marcas':marcas,
			'salones':salones,
			'marca_actual':actual,
			'actividades_semana':actividades_semana,
			'confirmados_semana':zip(confirmados_semana,enespera_semana,reservas_semana,cuposenespera_semana,pasado),
			'reservas_semana':reservas_semana,
			'enespera_semana':enespera_semana,
			'cuposenespera_semana':cuposenespera_semana,
			'disciplinas':disciplinas,
			'instructores':instructores,
			'notificacion':notificacion})
	else:
		nombre = request.user.get_full_name
		actividades_semana = []
		confirmados_semana = []
		reservas_semana = []
		enespera_semana = []
		cuposenespera_semana = []
		cuentas = []
		disciplinas = Disciplina.objects.all()
		for i in range(0, 8):
			p = Participantes.objects.values_list('pa_actividad',flat=True).filter(pa_usuario = request.user,pa_actividad__ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23)),)
			e = Espera.objects.values_list('es_actividad',flat=True).filter(es_usuario = request.user,es_actividad__ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23)),)
			pq = Actividad.objects.filter(pk__in=p)
			eq = Actividad.objects.filter(pk__in=e)
			q = []
			if perfil.u_entrenador:
				q = Actividad.objects.filter(ac_instructor=perfil,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23)))
				acthoy = (q|pq|eq).order_by('ac_hora_ini')
			else:
				acthoy = (pq|eq).order_by('ac_hora_ini')
			est = []
			cuentas.append(acthoy.count())
			for x in acthoy:
				if x in pq:
					est.append([1,Participantes.objects.get(pa_actividad=x,pa_usuario=request.user).pa_num_cupo])
				elif x in eq:
					est.append([2,Espera.objects.get(es_actividad=x,es_usuario=request.user).es_num_cupo])
				else:
					est.append([0])
			actividades_semana.append(zip(acthoy,est))
			confirmados_semana.append(Actividad.objects.filter(ac_instructor=perfil,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cupos_reservados'),0)))
			reservas_semana.append(Actividad.objects.filter(ac_instructor=perfil,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cap_max'),0)))
			enespera_semana.append(Actividad.objects.filter(ac_instructor=perfil,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cupos_en_espera'),0)))
			cuposenespera_semana.append(Actividad.objects.filter(ac_instructor=perfil,ac_fecha__range=(ini_sem+timedelta(days=i),ini_sem+timedelta(days=i,hours=23))).aggregate(sum_cupos=Coalesce(Sum('ac_cap_max_espera'),0)))
		maximo = max(cuentas)
		print(cuentas)
		print(maximo)
		minimo = list(map((lambda x: range(maximo-x) ), cuentas))
		print(minimo)
		return render(request, 'mi-calendario-atleta.html', {
			'dia_hoy':str(dia_hoy),
			'ini_sem':str(ini_sem.day),
			'inicio_sem':ini_sem,
			'mes':getmes(ini_sem.month-1),
			'pasada':pasada,
			'maximo':maximo,
			'fin_de_sem':fin_sem,
			'fin_sem':str(fin_sem.day),
			'nombre':nombre,
			'dia_sem':dia_sem,
			'minimo':minimo,
			'sem':sem,
			'pk':pk,
			'perfil':perfil,
			'sem_date':sem_date,
			'hoy':hoy,
			'notificaciones':getnotificacionesusuario(request.user,25),
			'actividades_semana':zip(actividades_semana,minimo),
			'marcas_publicas':marcas_publicas,
			'confirmados_semana':confirmados_semana,
			'reservas_semana':reservas_semana,
			'enespera_semana':enespera_semana,
			'cuposenespera_semana':cuposenespera_semana,
			'disciplinas':disciplinas,
			'notificacion':notificacion})
