from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.response import Response

#Models
from django.contrib.auth.models import User
from app_content.models import  *
from Users import *
from consejero_server import *
from user_interaction import *

class AppConfigurationSerializer(serializers.ModelSerializer):
	"""Serialializer for app basic configuration"""
	class Meta:
		model = ApplicationConfiguration
		fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
	"""Serializer for profile and User information"""

	class Meta:
		model = Profile
		fields = '__all__'
		depth = 1