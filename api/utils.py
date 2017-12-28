import os
import uuid
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
    msg = EmailMultiAlternatives(subject,message,CONCTACT_EMAIL,[email_contact_us],)
    msg.attach_alternative(message, "text/html")
    msg.send()


def password_generator():
    """Retorna un password único aleatorio.
    """
    return str(uuid.uuid1())[:3]

def email_password_recovery(email, password):
    print('recovery password for ' + email)
    subject = PASSWORD_RECOVERY_EMAIL_SUBJECT
    message = email + ' tu contraseña es: ' + password
    msg = EmailMultiAlternatives(subject,message, CONCTACT_EMAIL,[email],)
    msg.attach_alternative(message, "text/html")
    msg.send()
    #ToDo: implements this function async



USER_NOT_EXISTS = 'Usuario no existe'
USER_ACCOUNT_INACTIVE = 'Cuenta inactiva'
USER_CREDENTIALS_NOT_VALID = 'Las credenciales son inválidas'
USER_MISSING_EMAIL_OR_PASSWROD = 'Falta usuario y/o  contraseña'
PASSWORD_RECOVERY_SUCCESSFUL = 'A tu email llegará un correo con tu nueva contraseña'
PASSWORD_RECOVERY_EMAIL_SUBJECT = 'Conse - Recuperación de contraseña'
CONCTACT_EMAIL = 'no-responder@nrc.no'