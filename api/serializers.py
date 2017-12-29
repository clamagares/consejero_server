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
#from user_interaction import *
from user_interaction.models import *
from api import *
from api.strings import *
from api.errorcodes import *
from api.utils import *

class AppConfigurationSerializer(serializers.ModelSerializer):
	"""Serialializer for app basic configuration"""
	class Meta:
		model = ApplicationConfiguration
		fields = '__all__'

	def to_representation(self, instance):
		resp = {}
		resp['video_tutorial_id'] = instance.video_tutorial_id
		resp['emergency_message'] = instance.emergency_message
		resp['about_noruegan_council'] = instance.about_noruegan_council
		resp['terms_condition_url'] = instance.terms_condition_url
		resp['min_pin_length'] = instance.min_pin_length
		resp['psw_regular_expression'] = instance.psw_regular_expression
		resp['psw_error_recomendation'] = instance.psw_error_recomendation
		resp['document_type_list'] = DocumentTypeSerializer(DocumentType.objects.all(), many = True).data
		#print(str(resp['document_type_list']))
		resp['gender_list'] = GenderSerializer(Gender.objects.all(), many = True).data
		resp['state_list'] = StateSerializer(State.objects.all(), many = True).data
		resp['city_list'] = CitySerializer(City.objects.all(), many = True).data
		resp['condition_list'] = ConditionSerializer(Condition.objects.all(), many = True).data
		resp['ethnic_group_list'] = EthnicGroupSerializer(EthnicGroup.objects.all(), many = True).data
		resp['role_list'] = RoleSerializer(Role.objects.all(), many = True).data
		resp['body_part'] = BodyPartSerializer(BodyParts.objects.all(), many = True).data
		resp['avatar_pieces_list'] = AvatarPieceSerializer(AvatarPiece.objects.all(), many = True, context={'request': self.context['request']}).data
		resp['contact_form_type_list'] = ContactFormTypeSerializer(ContactFormTypes.objects.all(), many = True, context={'request': self.context['request']}).data
		resp['course_list'] = CourseSerializer(Courses.objects.all(), many = True, context={'request': self.context['request']}).data

		return resp


class TopicActivitySerializer(serializers.ModelSerializer):
	"""Topic Activity Serializer"""

	class Meta:
		model = TopicActivity
		fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):

	course = serializers.PrimaryKeyRelatedField(queryset = Courses.objects.all())

	class Meta:
		model = Topic
		fields = ('id','course','name','abreviature','description','icon','topic_activity_list')
		depth = 1

	def get_queryset(self, obj):
		return Topic.objects.all().order_by('-id')
		

class CourseSerializer(serializers.ModelSerializer):

	course_topics = serializers.SerializerMethodField()

	class Meta:
		model = Courses
		fields = ('id','name','abreviature','description','icon','course_topics')

	def get_course_topics(self, obj):

		orderder_queryset = Topic.objects.filter(course = obj).order_by('id')
		return TopicSerializer(orderder_queryset, context={'request': self.context['request']}, many = True).data
		

class UserTopicProgressSerializer(serializers.ModelSerializer):

	user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
	topic_activity = serializers.PrimaryKeyRelatedField(queryset = TopicActivity.objects.all())

	class Meta:
		model = UserTopicProgress
		fields = ('user','topic_activity','date_completed')


class DocumentTypeSerializer(serializers.ModelSerializer):
	"""Model to serializer document types"""

	class Meta:
		model = DocumentType
		fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
	"""Model to serializer Gender"""

	class Meta:
		model = Gender
		fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
	"""Model to serializer city"""

	state = serializers.CharField(read_only = True)

	class Meta:
		model = City
		fields = ('id','name', 'code','abreviature','state','description','icon',)

class StateSerializer(serializers.ModelSerializer):
	"""Model to serializer state"""

	class Meta:
		model = State
		fields = ('id','name', 'code','abreviature','description','icon',)

class ConditionSerializer(serializers.ModelSerializer):
	"""Model to serializer condition"""

	class Meta:
		model = Condition
		fields = '__all__'

class EthnicGroupSerializer(serializers.ModelSerializer):
	"""Model to serializer ethnic group"""

	class Meta:
		model = EthnicGroup
		fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
	"""Model to serializer role"""

	class Meta:
		model = Role
		fields = '__all__'

class BodyPartSerializer(serializers.ModelSerializer):
	"""Model to serializer body part"""

	class Meta:
		model = BodyParts
		fields = '__all__'

class AvatarPieceSerializer(serializers.ModelSerializer):
	"""Model to serializer avatar pieces"""

	class Meta:
		model = AvatarPiece
		fields = '__all__'

class ContactFormTypeSerializer(serializers.ModelSerializer):
	"""Model to serializer contact form types"""

	class Meta:
		model = ContactFormTypes
		fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
	"""Serializer for profile information"""

	first_name = serializers.CharField(write_only = True, required = False)
	last_name = serializers.CharField(write_only = True, required = False)

	class Meta:
		model = Profile
		exclude = ('user',)
		#fields = '__all__'
		depth = 1


# class ProfileUpdateSerializer(serializers.ModelSerializer):
# 	first_name = serializers.CharField(write_only = True, required = False)
# 	last_name = serializers.CharField(write_only = True, required = False)
# 	document_type = serializers.PrimaryKeyRelatedField(queryset = DocumentType.objects.all(), required = False)
# 	gender = serializers.PrimaryKeyRelatedField(queryset = Gender.objects.all(), required = False)
# 	ethnic_group = serializers.PrimaryKeyRelatedField(queryset = EthnicGroup.objects.all(), required = False)
# 	condition = serializers.PrimaryKeyRelatedField(queryset = Condition.objects.all(), required = False)
# 	role = serializers.PrimaryKeyRelatedField(queryset = Role.objects.all(), required = False)
# 	origin_city = serializers.PrimaryKeyRelatedField(queryset = City.objects.all(), required = False)


# 	class Meta:
# 		model = Profile
# 		exclude = ('user',)
# 		#fields = '__all__'
# 		depth = 1

# 	def update(self, instance, validated_data):
# 		user = instance.user

# 		#Updating user fields
# 		try:
# 			user.first_name = validated_data['first_name']
# 		except:
# 			print('No first_name updated')
# 		try:
# 			user.last_name = validated_data['last_name']
# 		except:
# 			print('No last_name updated')
# 		user.save()

# 		super(ProfileUpdateSerializer, self).update(instance, validated_data)

# 		return instance

# 	def to_representation(self, obj):

# 		user = obj.user
# 		resp = {}
# 		token = Token.objects.get(user = user)
# 		#profile = Profile.objects.get(user = obj)
# 		resp['token'] = token.key
# 		#profile_serializer = ProfileSerializer(Profile.objects.get(user = obj), many =  False)
# 		resp['profile'] = ProfileSerializer(instance= obj, many =  False).data
# 		resp['user'] = UserSerializer(instance = user, many =  False).data

# 		return resp 


class UserUpdatedProfileSerializer(serializers.Serializer):
	#Basic user data
	first_name = serializers.CharField(required = False)
	last_name = serializers.CharField(required = False)

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

	def update(self, instance, validated_data):
		#Updating user fields

		user = instance.user
		try:
			user.first_name = validated_data['first_name']
		except:
			print('No first_name updated')
		try:
			user.last_name = validated_data['last_name']
		except:
			print('No last_name updated')
		user.save()

		#Updating profile
		try:
			instance.document_type = DocumentType.objects.get(pk = validated_data['document_type'])
		except:
			print('No document_type updated')

		try:
			instance.gender = Gender.objects.get(pk = validated_data['gender'])
		except:
			print('No gender updated')
		try:
			instance.ethnic_group = EthnicGroup.objects.get(pk = validated_data['ethnic_group'])
		except:
			print('No ethnic_group updated')
		try:
			instance.condition = Condition.objects.get(pk = validated_data['condition'])
		except:
			print('No condition updated')
		try:
			instance.origin_city = City.objects.get(pk = validated_data['origin_city'])
		except:
			print('No origin_city updated')
		try:
			instance.role = Role.objects.get(pk = validated_data['role'])
		except:
			print('No role updated')

		try:
			instance.document_number = validated_data['document_number']
		except:
			print('No document_number updated')

		try:
			instance.birthdate = validated_data['birthdate']
		except:
			print('No birthdate updated')

		try:
			instance.isNRCBeneficiary = validated_data['isNRCBeneficiary']
		except:
			print('No isNRCBeneficiary updated')

		try:
			instance.contact_phone = validated_data['contact_phone']
		except:
			print('War: contact_phone missing')

		instance.save()

		return instance

	def to_representation(self, obj):

		user = obj.user
		resp = {}
		token = Token.objects.get(user = user)
		#profile = Profile.objects.get(user = obj)
		resp['token'] = token.key
		#profile_serializer = ProfileSerializer(Profile.objects.get(user = obj), many =  False)
		resp['profile'] = ProfileSerializer(instance= obj, many =  False).data
		resp['user'] = UserSerializer(instance = user, many =  False).data

		return resp 


class SosContactSerializer(serializers.ModelSerializer):
	"""Serializer for emergency contact model"""
	user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
	city = serializers.PrimaryKeyRelatedField(queryset = City.objects.all())
	class Meta:
		model = SosContact
		fields = ('user', 'city','name','email','contact_phone')
		depth = 1


class UserSerializer(serializers.ModelSerializer):
	"""Serializer for auth.user model"""
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name','username','email')


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
	document_number = serializers.CharField(required = False, allow_null = True, allow_blank = True)
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
			birthdate = validated_data['birthdate'],
			isNRCBeneficiary = validated_data['isNRCBeneficiary'])


		try:
			profile.document_number = validated_data['document_number']
		except:
			print('War: document_number missing')

		try:
			profile.document_type = DocumentType.objects.get(pk = validated_data['document_type'])
		except:
			print('War: document_type missing')

		try:
			profile.contact_phone = validated_data['contact_phone']
		except:
			print('War: contact_phone missing')

		profile.save()

		try:
			profile.ethnic_group = EthnicGroup.objects.get(id=validated_data['ethnic_group'])
		except:
			print('War: ethnic_group missing')
		profile.save()

		try:
			profile.condition = Condition.objects.get(id=validated_data['condition'])
		except:
			print('War: condition missing')
		profile.save()

		try:
			profile.origin_city = City.objects.get(id=validated_data['origin_city'])
		except:
			print('War: origin_city missing')
		profile.save()

		try:
			profile.role = RoleSerializer.objects.get(id=validated_data['role'])
		except:
			print('War: role missing')
		profile.save()


		#Creating Location instance
		try:
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
		except:
			print('War: actual_city missing')

		return user


	def to_representation(self, obj):
		resp = {}
		token = Token.objects.get(user = obj)
		profile = Profile.objects.get(user = obj)
		resp['token'] = token.key
		profile_serializer = ProfileSerializer(Profile.objects.get(user = obj), many =  False)
		resp['profile'] = ProfileSerializer(Profile.objects.get(user = obj), many =  False).data
		resp['user'] = UserSerializer(User.objects.get(username = obj.username), many =  False).data

		return resp


class UserAvatarSerializer(serializers.Serializer):
	"""Serializer for user avatar pieces"""
	user = serializers.IntegerField(write_only = True)
	avatar_piece = serializers.IntegerField(write_only = True)


	def create(self, validated_data):
		#Se personaliza para manejar que sol exista una pieza por parte del cuerpo y por usuario
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
		depth = 2


class ListUserAvatarSerializer(serializers.ListSerializer):
	child = UserAvatarSerializer()

	def to_representation(self, instance):
		return UserAvatarResponseSerializer(UserAvatar.objects.filter(user = self.context['request'].user), context={'request': self.context['request']}, many = True).data


class ContactFormSerializer(serializers.ModelSerializer):
	"""Serializer for contact form"""

	user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

	message_type = serializers.PrimaryKeyRelatedField(queryset = ContactFormTypes.objects.all())

	class Meta:
		model = ContactForm
		fields = '__all__'


class ListUserTopicProgress(serializers.ListSerializer):
	child = UserTopicProgressSerializer()




class UserLogginSerializer(serializers.Serializer):
	"""Serializer to loggin atempt"""

	email = serializers.EmailField()
	password = serializers.CharField()

	def validate(self, attrs):
		email = attrs.get('email')
		password = attrs.get('password')

		if email and password:
			# Check if user sent email
			try:
				user_request = User.objects.get(email=email.lower())
			except User.DoesNotExist:
				msg = (USER_NOT_EXISTS)
				raise CustomValidation(msg, 404)

			email = user_request.email.lower()

			#Validate user credentials
			user = authenticate(username=email.lower(), password=password)

			if user:
				#Validate user is active
				if not user.is_active:
					msg = (USER_ACCOUNT_INACTIVE)
					raise CustomValidation(msg, 404)
			else:
				msg = (USER_CREDENTIALS_NOT_VALID)
				raise CustomValidation(msg, 404)
				#raise exceptions.ValidationError(msg)
		else:
			msg = (USER_MISSING_EMAIL_OR_PASSWROD)
			raise CustomValidation(msg, 404)

		attrs['user'] = user
		return attrs

	def to_representation(self, obj):
		resp = {}
		token = Token.objects.get(user = obj)
		profile = Profile.objects.get(user = obj)
		resp['token'] = token.key
		profile_serializer = ProfileSerializer(Profile.objects.get(user = obj), many =  False)
		resp['profile'] = ProfileSerializer(Profile.objects.get(user = obj), many =  False).data
		resp['user'] = UserSerializer(User.objects.get(username = obj.username), many =  False).data
		return resp

class SimplePostResponseSerializer(serializers.Serializer):

    detail = serializers.CharField()
    

class PasswordRecoverySerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate_email(self, value):
		if User.objects.filter(email=value.lower()):
			return value
		else:
			msg = (USER_NOT_EXISTS)
			raise CustomValidation(msg, 404)
		#return value


class DocumentTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('id','name','description','date','code','url','extension','icon','file')

class DocumentLibrarySerializer(serializers.ModelSerializer):
	"""Serializer for the library docs and types"""
	document_by_type = DocumentTextSerializer(many = True, read_only = True)

	class Meta:
		model = DocumentTextType
		fields = ('id','course','name','abreviature','description','icon','document_by_type',)
