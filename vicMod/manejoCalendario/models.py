from django.db import models

class Relacion(models.Model):
	SOLICITUDES_CHOICES = (
        ('A', 'Aprobada'),
        ('R', 'Rechazada'),
        ('P', 'Pendiente'),)
	r_user = models.ForeignKey('auth.User')
	r_marca = models.ForeignKey('Marca')
	r_estado = models.CharField(max_length=1, choices=SOLICITUDES_CHOICES,default='P',)
	r_entrenador = models.BooleanField(default=False)

	def __str__(self):
		return str(self.r_marca)

class Actividad(models.Model):
	ESTADOS_CHOICES = (
        ('Planifico', 'Planifico'),
        ('Abierta Reversible', 'Abierta Reversible'),
        ('Abierta Irreversible', 'Abierta Irreversible'),
        ('Cerrada', 'Cerrada'),
        ('Activa', 'Activa'),
        ('Culminada', 'Culminada'),
        ('Cancelada', 'Cancelada'))
	ac_nombre = models.CharField(max_length=200)
	ac_disciplina = models.ForeignKey('Disciplina')
	ac_fecha = models.DateField()
	ac_estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES,default='Planifico',)
	ac_hora_ini = models.TimeField()
	ac_hora_fin = models.TimeField()
	ac_salon = models.ForeignKey('Salon')
	ac_marca = models.ForeignKey('Marca')
	ac_instructor = models.ForeignKey('UserProfile')
	ac_descripcion = models.TextField()
	ac_cap_min = models.IntegerField(default= 0)
	ac_cap_max = models.IntegerField(default = 100)
	ac_requisitos = models.TextField()
	ac_cupos_reservados = models.IntegerField(default = 0)
	ac_cap_max_espera = models.IntegerField(default = 100)
	ac_cupos_en_espera = models.IntegerField(default = 0)
	ac_precio = models.IntegerField(default = 1)
	ac_bono = models.IntegerField(default = 0)
	ac_creditos = models.IntegerField(default = 1)

	def __str__(self):
		return str(self.ac_nombre)

class Salon(models.Model):
	s_nombre = models.CharField(max_length=100)
	s_capacidad = models.IntegerField()
	s_marca = models.ForeignKey('Marca',default=0)

	def __str__(self):
		return str(self.s_nombre.encode('utf-8'))

class Participantes(models.Model):
	pa_actividad = models.ForeignKey('Actividad')
	pa_usuario = models.ForeignKey('auth.User')
	pa_num_cupo = models.IntegerField()
	pa_asistencia = models.BooleanField(default=False)
	pa_cobrado = models.BooleanField(default=False)
	pa_plan = models.ForeignKey('Planes')

	def __str__(self):
		return str(self.pa_actividad.ac_nombre+" - "+self.pa_usuario.username)

class Serie(models.Model):
	tipos = (
        ('LM', 'Lunes, Miercoles y Viernes'),
        ('MJ', 'Martes y Jueves'),
        ('LV', 'Lunes a Viernes'),
        ('DI', 'Diario'),
        ('SM', 'Semanal'),    )
	fin = (
        ('D', 'Terminar en la fecha'),
        ('R', 'Despues de'),)
	s_actividad = models.ForeignKey('Actividad')
	s_num_ser = models.CharField(max_length=50)
	s_tipo = models.CharField(max_length=2, choices=tipos)
	s_cada = models.IntegerField(default=0)
	s_lunes = models.BooleanField(default=False)
	s_martes = models.BooleanField(default=False)
	s_miercoles = models.BooleanField(default=False)
	s_jueves = models.BooleanField(default=False)
	s_viernes = models.BooleanField(default=False)
	s_sabado = models.BooleanField(default=False)
	s_domingo = models.BooleanField(default=False)
	s_empieza = models.DateField(default=datetime.now())
	s_termina = models.CharField(max_length=1,choices=fin)
	s_termina_date = models.DateField(default=datetime.now())
	s_termina_int = models.IntegerField(default=20)


	def __str__(self):
		return self.s_num_ser+" - "+str(self.s_actividad)

class Espera(models.Model):
	es_actividad = models.ForeignKey('Actividad')
	es_usuario = models.ForeignKey('auth.User')
	es_num_cupo = models.IntegerField()
	es_plan= models.ForeignKey('Planes')

	def __str__(self):
		return str(self.es_actividad.ac_nombre+" - "+self.es_usuario.username)

class Notificacion(models.Model):
	OPCIONES_CHOICES = (
        ('R', 'Reserva'),
        ('E', 'Espera'),
        ('S', 'Solicitud'),
        ('P','Pago'),
        ('A','Actividad'),
        ('C','Compra'),)
	n_notificador = models.ForeignKey('auth.User')
	n_actividad = models.ForeignKey('Actividad',blank=True,null=True)
	n_fecha = models.DateTimeField(auto_now_add=True, blank=True)
	n_contenido = models.CharField(max_length=50)
	n_tipo = models.CharField(max_length=1,choices=OPCIONES_CHOICES)
	n_marca = models.ForeignKey('Marca')


