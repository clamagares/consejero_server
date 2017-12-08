import os
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from app_content.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class CustomValidation(APIException):
    """Returns personalized code and message to a failed request"""
    status_code = 400
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {'detail': force_text(detail)}
        else: 
            self.detail = {'detail': force_text(self.default_detail)}


def send_contact_email(contact_form):
    subject = contact_form.message_type.name + " - Mensaje Contacto Conse"
    message = contact_form.detail
    #message = user.first_name + ' tu contraseña es: ' + password
    email_contact_us = ApplicationConfiguration.objects.get(id = 1).email_contact_us
    msg = EmailMultiAlternatives(subject,message, "contac@consejo.nrc.org.co",[email_contact_us],)
    msg.attach_alternative(message, "text/html")
    msg.send()