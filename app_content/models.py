from django.db import models

# Create your models here.

class ApplicationConfiguration(models.Model):
	"""Model for application configuration"""
	video_tutorial_id = models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'ID Youtube Video Tutorial')
	emergency_message = models.TextField(verbose_name = 'Plantilla de mensaje de emergencia')
	about_noruegan_council = models.TextField(verbose_name = 'Acerca del NRC')
	email_contact_us = models.EmailField(max_length = 150, verbose_name = 'Email de recepción mensajes de contacto')
	debug_mode = models.BooleanField(default = True, verbose_name = 'Habilitar modo debug')
	min_pin_length = models.SmallIntegerField(verbose_name = 'Longitud mínima de pin')


class NewsCategory(models.Model):
	"""News category model"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	abreviature = models.CharField(max_length = 100, verbose_name = 'Abreviatura', blank = True, null = True)
	description = models.TextField(null = True, blank = True, verbose_name = 'Descripción')
	icon = models.ImageField(
		upload_to = 'app_images/new_category_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		verbose_name = 'Ícono')


class ContentTags(models.Model):
	"""Tags for the content"""
	name = models.CharField(max_length = 100, verbose_name = 'Nombre')
	icon = models.ImageField(
		upload_to = 'app_images/tags_icon',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		verbose_name = 'Ícono')

class NewsTags(models.Model):
	"""Relation between news and tags"""
	tag = models.ForeignKey('ContentTags', verbose_name = 'Tag asociado')
	new = models.ForeignKey('NewsFeed', related_name = 'news_tags', verbose_name = 'Noticia asociada')


class NewsFeed(models.Model):
	"""Model for neews to publish"""
	category = models.ForeignKey('NewsCategory', related_name = 'news_category', verbose_name = 'Categoria')
	tittle = models.CharField(max_length = 150, verbose_name = 'Título')
	abstract = models.CharField(max_length = 200, blank = True, null = True, verbose_name = 'Vista previa/Resumen')
	detail = models.TextField(verbose_name = 'Detalle')
	more_info_link = models.URLField(blank = True, null = True, verbose_name = 'Link para más información')
	image = models.ImageField(
		upload_to = 'app_images/news_feed_images',
		max_length = 255, 
		help_text = '200x200 píxeles', 
		null = True,
		verbose_name = 'Imagen')
	published = models.BooleanField(default = False, verbose_name = 'Publicado?')
	since = models.DateTimeField(verbose_name = 'Publicado desde')
	until = models.DateTimeField(verbose_name = 'Publicado hasta')
	priority = models.IntegerField(verbose_name = 'Prioridad')
	created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de creación')
	created_by = models.ForeignKey('auth.User', verbose_name = 'Usuario creador')






