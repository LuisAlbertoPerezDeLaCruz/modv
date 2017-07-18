from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator

class Ciudad(models.Model):
	c_nombre = models.CharField(primary_key=True,max_length=30)

	def __str__(self):
			return str(self.c_nombre)

class Zona(models.Model):
	z_ciudad = models.ForeignKey(Ciudad)
	z_municipio = models.CharField(primary_key=True,max_length=30)

	def __str__(self):
			return str(self.z_municipio)

class Marca(models.Model):
    CURRENCY_CHOICES = (
        ('$  ', '$'),
        ('Bs.', 'Bs.'),
        ('€  ', '€'),)
    m_nombre = models.CharField(max_length=200)
    m_alias = models.CharField(max_length=30)
    m_direccion = models.TextField()
    m_ciudad = models.ForeignKey('Ciudad')
    m_municipio = models.ForeignKey('Zona')
    m_correo = models.EmailField(max_length=70, blank=True, default='victrois@gmail.com')
    m_telefono1 = models.ForeignKey('Phone', related_name='principal')
    m_telefono2 = models.ForeignKey('Phone')
    m_razon_social = models.CharField(max_length=150)
    m_doc_ident = models.CharField(max_length=30)
    m_descripcion = models.TextField()
    m_public = models.BooleanField(default=True)
    m_moneda = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='Bs.', )
    m_boletin = models.BooleanField(default=True)
    m_est_irrev = models.IntegerField(default=2)
    m_est_rrev = models.IntegerField(default=4)

    def __str__(self):
        return str(self.m_nombre)

class Dueno(models.Model):
    d_user = models.ForeignKey('auth.User')
    d_marca = models.ForeignKey('Marca')

    def __str__(self):
        return str(self.d_user) + " " + str(self.d_marca)

class Phone(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El telefono debe estar en formato: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list

    def __str__(self):
        return str(self.phone_number)

class Disciplina(models.Model):
    d_nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.d_nombre)

class UserProfile(models.Model):
    u_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name="profile")
    u_secondname = models.CharField(max_length=30)
    u_secondlastname = models.CharField(max_length=30)
    u_telefono = models.ForeignKey('Phone')
    u_alias = models.CharField(max_length=100)
    u_direccion = models.TextField()
    u_fecha_nac = models.DateField(default=datetime.now, blank=True)
    u_entrenador = models.BooleanField(default=False)
    u_marca = models.BooleanField(default=False)
    u_displinafav1 = models.ForeignKey('Disciplina', related_name='fav1', null=True)
    u_displinafav2 = models.ForeignKey('Disciplina', related_name='fav2', null=True)
    u_displinafav3 = models.ForeignKey('Disciplina', related_name='fav3', null=True)

    def __str__(self):
        return str(self.u_user)

    def get_User(self, Users):
        if Users == None:
            return None
        else:
            up = []
            for User in Users:
                up.append(UserProfile.objects.get(u_user__pk=User))
            return up
