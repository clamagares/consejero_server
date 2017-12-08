from django.contrib import admin
from user_interaction.models import *

# Register your models here.

admin.site.register(Topic)
admin.site.register(TopicActivity)
admin.site.register(UserTopicProgress)
admin.site.register(ContactForm)
admin.site.register(EmergencyAlerts)
admin.site.register(ContactFormTypes)