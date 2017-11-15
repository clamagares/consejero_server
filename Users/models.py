from django.db import models

# Create your models here.
from django.contrib.auth.models import User



class Role(models.Model):
	"""Atomic model for profile NRC personalized segmentation"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/role_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name


class EthnicGroup(models.Model):
	"""Atomic model for profile NRC personalized segmentation for ethnic group"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/ethinic_group_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class Condition(models.Model):
	"""Atomic model for profile NRC personalized segmentation for user condition"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/condition_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class DocumentType(models.Model):
	"""Atomic model for identification document types"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/document_type_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name


class Country(models.Model):
	"""Atomic model for country"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	international_code = models.CharField(max_length = 100, verbose_name = 'Código internacional', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/country_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class State(models.Model):
	"""Model for the state - user location"""
	country = models.ForeignKey('Country', related_name = 'state_country', verbose_name = 'País')
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	code = models.CharField(max_length = 100, verbose_name = 'Código', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/state_location_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class City(models.Model):
	"""Model for cities - user location"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	state = models.ForeignKey('State', related_name = 'city_state', verbose_name = 'Estado/Depto')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	code = models.CharField(max_length = 100, verbose_name = 'Código', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/city_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return str(self.state) + '-' + self.name

class Gender(models.Model):
	"""Atomic class for user gender segmentation"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	icon = models.ImageField(
		upload_to = 'app_images/gender_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class LocationType(models.Model):
	"""Atomic model for user location type, to allow segmentation"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/location_type_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class Location(models.Model):
	"""User location register"""
	city = models.ForeignKey('City', null = True, blank = True, related_name = 'location_cities', verbose_name = 'Ciudad')
	user = models.ForeignKey('auth.User', related_name = 'user_locations', verbose_name = 'Usuario')
	location_type = models.ForeignKey('LocationType', null =  True, blank = True, verbose_name = 'Tipo de locación')
	address = models.CharField(max_length = 100, null = True, blank = True, verbose_name = 'Dirección')
	phone_number = models.CharField(max_length = 100, null = True, blank = True, verbose_name = 'Teléfono')
	latitude = models.DecimalField(max_digits = 9, decimal_places = 6, null = True, blank = True, verbose_name = 'Latitud')
	longitude = models.DecimalField(max_digits = 9, decimal_places = 6, null = True, blank = True, verbose_name = 'Longitud')
	date_created = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de creación')

	def __str__(self):
		return str(self.date_created) + '-' + str(self.user)

class BodyParts(models.Model):
	"""Atomic model for create user avatar"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/body_part_icon', 
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class AvatarPiece(models.Model):
	"""Options of body parts for avatar creation"""
	body_part = models.ForeignKey('BodyParts', related_name = 'body_part_options', verbose_name = 'Parte del cuerpo')
	gender = models.ForeignKey('Gender', blank = True, null = True, related_name = 'genders', verbose_name = 'Género')
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/avatar_pieces_icon',
		max_length = 255, 
		help_text = '300x300 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return str(self.body_part) + '-' + self.name

class UserAvatar(models.Model):
	"""Model for save the user avatar combination"""
	user = models.ForeignKey('auth.User', related_name = 'user_avatar', verbose_name = 'Usuario')
	avatar_piece = models.ForeignKey('AvatarPiece', related_name = 'user_avatar_piece', verbose_name = 'Pieza seleccionada')

	def __str__(self):
		return str(self.user) + '-' + str(self.avatar_piece)

class Profile(models.Model):
	"""Model to complete the user info related with the app"""

	user = models.OneToOneField(
		'auth.User',
		verbose_name = 'Usuario')
	role = models.ForeignKey('Role', null = True, blank = True, related_name = 'profile_role', verbose_name = 'Rol')
	gender = models.ForeignKey('Gender', related_name = 'profile_gender', verbose_name = 'Género')
	ethnic_group = models.ForeignKey('EthnicGroup', null = True, blank = True, related_name = 'profile_ethnic_group', verbose_name = 'Grupo Étnico')
	condition = models.ForeignKey('Condition', null = True, blank = True, related_name = 'profile_condition', verbose_name = 'Condición')
	document_type = models.ForeignKey('DocumentType', null = True, blank = True, verbose_name = 'Tipo de documento')
	document_number = models.CharField(max_length = 50, null = True, blank = True, verbose_name = 'Número de documento')
	birthdate = models.DateField(null = True, blank = True, verbose_name = 'Fecha de nacimiento')
	isNRCBeneficiary = models.BooleanField(default = False, verbose_name = 'Es beneficiario NRC')
	origin_city = models.ForeignKey('City', null = True, blank = True, related_name = 'profile_origin_city', verbose_name = 'Ciudad de origen')
	contact_phone = models.CharField(max_length = 50, null = True, blank = True, verbose_name = 'Teléfono de contacto')

	def __str__(self):
		return str(self.user)


class SosContact(models.Model):
	"""Users emergency contacts"""
	user = models.ForeignKey('auth.User',related_name = 'users_emergency_contact', verbose_name = 'Usuario')
	city = models.ForeignKey('City', null = True, blank = True, related_name = 'sos_cities', verbose_name = 'Ciudad')
	name = models.CharField(max_length = 70, verbose_name = 'Nombre y apellido')
	email = models.EmailField(max_length = 240)
	contact_phone = models.CharField(max_length = 50, null = True, blank = True, verbose_name = 'Teléfono')

	def __str__(self):
		return str(self.user) + '-' + self.name


