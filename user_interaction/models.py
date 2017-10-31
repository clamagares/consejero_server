from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
	"""Course in the app"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/topics_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class TopicActivity(models.Model):
	"""The activities in the course to get the user progress"""
	topic = models.ForeignKey('Topic', verbose_name = 'Curso')
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	ponderation_progress = models.SmallIntegerField(default = 1, verbose_name = 'Ponderación sobre el progreso (Defecto = 1)')
	icon = models.ImageField(
		upload_to = 'app_images/activities_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name + '-' + str(self.topic)


class UserTopicProgress(models.Model):
	"""The user completed activities"""
	user = models.ForeignKey('auth.User', verbose_name = 'Usuario')
	topic_activity = models.ForeignKey('TopicActivity', verbose_name = 'Actividad')
	date_completed = models.DateTimeField(verbose_name = 'Fecha de ejecución')
	date_created = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de creación')

	def __str__(self):
		return str(self.user) + '-' + str(self.topic_activity)


class ContactForm(models.Model):
	"""The user contact message model"""
	user = models.ForeignKey('auth.User', verbose_name = 'Usuario')
	subject = models.CharField(max_length = 200, verbose_name = 'Asunto')
	detail = models.TextField(verbose_name = 'Detalle')
	date_sent = models.DateTimeField(verbose_name = 'Fecha de envío')
	date_receipt = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de recepción')

	def __str__(self):
		return str(self.date_sent) + '-' + str(self.user) + '-' + self.subject


class EmergencyAlerts(models.Model):
	"""The user emergency alerts model"""
	user = models.ForeignKey('auth.User', verbose_name = 'Usuario')
	date_sent = models.DateTimeField(verbose_name = 'Fecha de envío')
	date_receipt = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de recepción')
	city = models.ForeignKey('Users.City', null = True, blank = True, 
		related_name = 'emergency_alert_cities', verbose_name = 'Ciudad')
	latitude = models.DecimalField(max_digits = 9, decimal_places = 6, 
		null = True, blank = True, verbose_name = 'Latitud')
	longitude = models.DecimalField(max_digits = 9, decimal_places = 6, 
		null = True, blank = True, verbose_name = 'Longitud')

	def __str__(self):
		return str(self.date_sent) + '-' + str(self.user)