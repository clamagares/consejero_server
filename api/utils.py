import os
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text

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