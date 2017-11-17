from django.shortcuts import render

# Create your views here.
import math
from django.shortcuts import render
from rest_framework import parsers
from rest_framework.parsers import JSONParser
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIAccess
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from api.permissions import *
from api.serializers import *

class ApplicationConfigurationView(generics.ListAPIView):
	"""Get the application basic configuration"""
	queryset = ApplicationConfiguration.objects.all()
	serializer_class = AppConfigurationSerializer


class UsersView(generics.RetrieveUpdateDestroyAPIView):
	"""View for get the user info"""
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = (IsOwner,)

class CreateUsersView(generics.CreateAPIView):
	"""View to create user and profile"""
	queryset = User.objects.all()
	serializer_class = UserProfileCreateSerializer
	
class EmergencyContactsView(generics.ListCreateAPIView):
	"""View for get the emergency contacts info"""

	serializer_class = SosContactSerializer
	permission_classes = (IsOwner,)

	def get_queryset(self):
		user = self.request.user
		return SosContact.objects.filter(user = user)

class EmergencyContactEdit(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsOwner,)
	queryset = SosContact.objects.all()
	serializer_class = SosContactSerializer


class UserAvatarPieces(generics.ListCreateAPIView):
	"""View to create or get the list of the user avatar pieces"""
	permission_classes = (IsOwner,)
	queryset = UserAvatar.objects.all()
	serializer_class = ListUserAvatarSerializer
	

	# def list(self, request):
	# 	# Note the use of `get_queryset()` instead of `self.queryset`
	# 	queryset = self.get_queryset()
	# 	serializer = UserAvatarSerializer(queryset, many=True)
	# 	return Response(serializer.data)