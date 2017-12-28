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

class ApplicationConfigurationView(generics.RetrieveAPIView):
	"""Get the application basic configuration"""
	queryset = ApplicationConfiguration.objects.all()
	serializer_class = AppConfigurationSerializer


class UsersView(generics.RetrieveUpdateDestroyAPIView):
	"""View for get the user info"""
	queryset = Profile.objects.all()
	serializer_class = UserUpdatedProfileSerializer
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



class ContactForm(generics.CreateAPIView):
	"""View to create contact forms"""

	queryset = ContactForm.objects.all()
	serializer_class = ContactFormSerializer


class SaveUserProgress(generics.ListCreateAPIView):
	"""View to save user activity progress"""

	serializer_class = ListUserTopicProgress
	permission_classes = (IsOwner,)

class GetLibraryDocs(generics.ListCreateAPIView):
	"""View to get the library docs"""
	serializer_class = DocumentLibrarySerializer
	queryset = DocumentTextType.objects.all()


class AuthUser(APIView):
	"""Api view for loggin user"""
	parser_classes = (
		parsers.FormParser,
		parsers.MultiPartParser,
		parsers.JSONParser,
	)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = UserLogginSerializer

	def post(self, request):
		serializer = UserLogginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data['email']
		password = serializer.validated_data['password']
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		content = {}
		ser = UserLogginSerializer(user)
		return Response(ser.data)


class PostPasswordRecovery(APIView):
    """Api view for recovery password"""
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = PasswordRecoverySerializer

    def post(self, request):
        serializer = PasswordRecoverySerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email = email)
        password = user.first_name + password_generator()
        user.set_password(password)
        user.save()
        email_password_recovery(email, password)
        response = SimplePostResponseSerializer(data = {'detail' : PASSWORD_RECOVERY_SUCCESSFUL})
        response.is_valid()
        return Response(response.data)