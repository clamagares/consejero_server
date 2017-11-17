from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

#Models
from django.contrib.auth.models import User
from app_content.models import  *
#from Users import *
from Users.models import *
from consejero_server import *
from user_interaction import *
from api import *
from api.strings import *
from api.errorcodes import *
from api.utils import *

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

class SosContactSerializer(serializers.ModelSerializer):
	"""Serializer for emergency contact model"""
	user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
	city = serializers.PrimaryKeyRelatedField(queryset = City.objects.all())
	class Meta:
		model = SosContact
		fields = ('user', 'city','name','email','contact_phone')
		depth = 1


class UserProfileCreateSerializer(serializers.Serializer):
	"""Serializer to create new user and profile"""

	#Basic user data
	first_name = serializers.CharField()
	last_name = serializers.CharField()
	email = serializers.EmailField()
	password = serializers.CharField()

	#NRC Segmentation data
	role = serializers.IntegerField(required = False)
	gender = serializers.IntegerField(required = False)
	ethnic_group = serializers.IntegerField(required = False)
	condition = serializers.IntegerField(required = False)
	birthdate = serializers.DateField(required = False)
	document_type = serializers.IntegerField(required = False)
	document_number = serializers.CharField(required = False)
	contact_phone = serializers.CharField(required = False)
	origin_city = serializers.IntegerField(required = False)
	isNRCBeneficiary = serializers.BooleanField(default = False)

	#Principal location
	actual_city = serializers.IntegerField(required = False)
	address = serializers.CharField(required = False)
	latitude = serializers.DecimalField(required = False, max_digits = 9, decimal_places = 6)
	longitude = serializers.DecimalField(required = False, max_digits = 9, decimal_places = 6)

	def validate_email(self, value):
		if User.objects.filter(email = value):
			msg = (USER_ALREADY_EXISTS)
			raise CustomValidation(msg,FORBIDDEN)
		return value


	def create(self, validated_data):
		#Creating User Model
		user = User.objects.create(username = validated_data['email'])
		user.first_name = validated_data['first_name']
		user.last_name = validated_data['last_name']
		user.email = validated_data['email']
		user.set_password(validated_data['password'])
		user.save()

		#Create Token
		token, created = Token.objects.get_or_create(user=user)

		#Creating Profile instance
		gender = Gender.objects.get(pk = validated_data['gender'])
		profile = Profile.objects.create(
			user = user, 
			gender = gender,
			document_number = validated_data['document_number'],
			birthdate = validated_data['birthdate'],
			isNRCBeneficiary = validated_data['isNRCBeneficiary'])
		profile.ethnic_group = EthnicGroup.objects.get(pk = validated_data['ethnic_group'])
		profile.condition = Condition.objects.get(pk = validated_data['condition'])
		profile.document_type = DocumentType.objects.get(pk = validated_data['document_type'])
		profile.origin_city = City.objects.get(pk = validated_data['origin_city'])

		try:
			profile.contact_phone = validated_data['contact_phone']
		except:
			print('War: contact_phone missing')
		profile.save()

		#Creating Location instance
		location_city = City.objects.get(pk = validated_data['actual_city'])
		location = Location.objects.create(city = location_city, user = user)
		try:
			location.location_type = LocationType.objects.get(pk = validated_data['location_type'])
		except:
			print('War: location_type missing')
		try:
			location.address = validated_data['address']
		except:
			print('War: address missing')
		try:
			location.latitude = validated_data['latitude']
		except:
			print('War: latitude missing')
		try:
			location.longitude = validated_data['longitude']
		except:
			print('War: longitude missing')
		try:
			location.phone_number = validated_data['contact_phone']
		except:
			print('War: phone_number missing')	

		location.save()

		return user




class UserAvatarSerializer(serializers.Serializer):
	"""Serializer for user avatar pieces"""
	user = serializers.IntegerField(write_only = True)
	avatar_piece = serializers.IntegerField(write_only = True)


	def create(self, validated_data):
		piece = AvatarPiece.objects.get(pk = validated_data['avatar_piece'])
		#print('encontrado piece' + str(piece))
		user = User.objects.get(pk = validated_data['user'])
		#print('encontrado user' + str(user))
		try:
			user_avatar = UserAvatar.objects.get(user = user, avatar_piece__body_part = piece.body_part)
			#print('encontrado user_avatar' + str(user_avatar))
			user_avatar.avatar_piece = piece
		except:
			user_avatar = UserAvatar.objects.create(user = user, avatar_piece = piece)
			#print('creado user_avatar' + str(user_avatar))
		user_avatar.save()
		#print('guardado user_avatar' + str(user_avatar))
		return user_avatar


class UserAvatarResponseSerializer(serializers.ModelSerializer):
	"""Serializer for response to avatar pieces creation"""

	user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
	avatar_piece = serializers.PrimaryKeyRelatedField(queryset = AvatarPiece.objects.all())

	class Meta:
		model = AvatarPiece
		fields = ('user', 'avatar_piece',)



class ListUserAvatarSerializer(serializers.ListSerializer):
	child = UserAvatarSerializer()

