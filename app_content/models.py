from django.db import models
from Users.models import *
from django.contrib.auth.models import User
from user_interaction.models import *

# Create your models here.

class ApplicationConfiguration(models.Model):
	"""Model for application configuration"""
	video_tutorial_id = models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'ID Youtube Video Tutorial')
	emergency_message = models.TextField(verbose_name = 'Plantilla de mensaje de emergencia')
	about_noruegan_council = models.TextField(verbose_name = 'Acerca del NRC')
	terms_condition_url = models.URLField(verbose_name = 'URL Términos y condiciones', blank = True, null = True)
	email_contact_us = models.EmailField(max_length = 150, verbose_name = 'Email de recepción mensajes de contacto')
	debug_mode = models.BooleanField(default = True, verbose_name = 'Habilitar modo debug')
	min_pin_length = models.SmallIntegerField(verbose_name = 'Longitud mínima de pin')
	psw_regular_expression = models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'Expresión regular contraseña')
	psw_error_recomendation =models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'Mensaje para expresión de contraseña')
	radius_shell_filter = models.IntegerField(blank = True, null = True, verbose_name = 'Radio de filtro de Escudos [km]')

	def __str__(self):
		return self.video_tutorial_id


class NewsCategory(models.Model):
	"""News category model"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/news_category_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name


class ContentTags(models.Model):
	"""Tags for the content"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	icon = models.ImageField(
		upload_to = 'app_images/tags_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name


class NewsTags(models.Model):
	"""Relation between news and tags"""
	tag = models.ForeignKey('ContentTags', verbose_name = 'Tag asociado')
	new = models.ForeignKey('NewsFeed', related_name = 'news_tags', verbose_name = 'Noticia asociada')

	def __str__(self):
		return tr(self.tag) + '-' + str(self.new)


class NewsFeed(models.Model):
	"""Model for neews to publish"""
	category = models.ForeignKey('NewsCategory', related_name = 'news_category', verbose_name = 'Categoria')
	tittle = models.CharField(max_length = 150, verbose_name = 'Título')
	#abstract = models.CharField(max_length = 200, blank = True, null = True, verbose_name = 'Vista previa/Resumen')
	#detail = models.TextField(verbose_name = 'Detalle')
	city = models.ForeignKey('Users.City', null = True, blank = True, verbose_name = 'Ciudad', related_name = 'news_by_city')
	more_info_link = models.URLField(blank = True, null = True, verbose_name = 'URL')
	#image = models.ImageField(
	#	upload_to = 'app_images/news_feed_images',
	#	max_length = 255, 
	#	help_text = '200x200 píxeles', 
	#	null = True,
	#	verbose_name = 'Imagen')
	#published = models.BooleanField(default = False, verbose_name = 'Publicado?')
	#since = models.DateTimeField(verbose_name = 'Publicado desde')
	#until = models.DateTimeField(verbose_name = 'Publicado hasta')
	#priority = models.IntegerField(verbose_name = 'Prioridad')
	#created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de creación')
	#created_by = models.ForeignKey('auth.User', verbose_name = 'Usuario creador')

	def __str__(self):
		return str(self.category) + '-' + self.tittle

class DocumentTextType(models.Model):
	"""Atomic model for document cateogries"""
	course = models.ForeignKey('user_interaction.Courses', verbose_name = 'Categoría de curso', null = True, blank = True, related_name = 'courses_docs_types')
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/document_category_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name + " - " + str(self.course)


class Document(models.Model):
	"""Model for files in the library"""
	doc_type = models.ForeignKey('DocumentTextType', verbose_name = 'Tipo de documento', related_name = 'document_by_type')
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	date = models.CharField(max_length = 50,null = True, blank = True, verbose_name = 'Fecha de documento')
	code = models.TextField(null = True, blank = True, verbose_name = 'Código')
	url = models.URLField(null = True, blank = True, verbose_name = 'URL')
	extension = models.CharField(max_length = 10,null = True, blank = True, verbose_name = 'Extensión')
	icon = models.ImageField(
		upload_to = 'app_images/documents_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')
	file = models.FileField(upload_to = 'Library', verbose_name = 'Archivo', null = True, blank = True)

	def __str__(self):
		return str(self.doc_type) + '-' + self.name

class DocumentTags(models.Model):
	"""Relation between document and tags"""
	tag = models.ForeignKey('ContentTags', verbose_name = 'Tag asociado')
	document = models.ForeignKey('Document', related_name = 'document_tags', verbose_name = 'Documento asociado')

	def __str__(self):
		return self.tag + '-' + str(self.document)


class OrganizationType(models.Model):
	"""Atomic model for Organization cateogries"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/organizations_category_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name

class Organization(models.Model):
	"""Model for organizations"""
	organization_type = models.ForeignKey('OrganizationType', verbose_name = 'Tipo de Organización')
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	url = models.URLField(null = True, blank = True, verbose_name = 'Página Web')
	icon = models.ImageField(
		upload_to = 'app_images/orgnizations_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name


class CorporatePhoneBook(models.Model):
	"""Model for organization branch offices"""
	organization_type = models.ForeignKey('OrganizationType', null = True, blank = True, verbose_name = 'Tipo de Organización', related_name = 'organization_by_type')
	city = models.ForeignKey('Users.City', verbose_name = 'Ciudad', null = True, blank = True)
	name = models.CharField(max_length = 300, null = True, blank = True,verbose_name = 'Nombre')
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	phone = models.CharField(max_length = 50, null = True, blank = True, verbose_name = 'Teléfono')
	mobile_phone = models.CharField(max_length = 50, null = True, blank = True, verbose_name = 'Móvil')
	address = models.TextField(max_length = 150, null = True, blank = True, verbose_name = 'Dirección')
	url = models.URLField(null = True, blank = True, verbose_name = 'Página Web')
	twitter = models.CharField(max_length = 150, null = True, blank = True, verbose_name = 'Twitter')
	email = models.EmailField(null = True, blank = True, verbose_name = 'Email de contacto')
	schedule = models.TextField(null = True, blank = True, verbose_name = 'Horario')
	latitude = models.DecimalField(max_digits = 9, decimal_places = 7, null = True, blank = True, verbose_name = 'Latitud')
	longitude = models.DecimalField(max_digits = 9, decimal_places = 7, null = True, blank = True, verbose_name = 'Longitud')
	icon = models.ImageField(
		upload_to = 'app_images/organization_branch_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		blank = True,
		verbose_name = 'Ícono')

	def __str__(self):
		return self.name + '-' + str(self.city)
