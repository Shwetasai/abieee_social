from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .manager import UserManager
from django.core.exceptions import ValidationError
import re
class User(AbstractUser):
    username=None
    def validate_phone(phone_number):
        errors = []
 
        if not phone_number.isdigit():
            errors.append('Phone number must contain only digits.')
        if not phone_number.startswith('05'):
            errors.append('Phone number must start with "05".')
        if len(phone_number) != 10 or not re.match(r'^\d{10}$', phone_number):
            errors.append('Phone number must be exactly 10 digits long')
        if errors:
            raise ValidationError(errors)
        return phone_number
    phone_number = models.CharField(max_length=15, blank=False,null=False,validators=[validate_phone], unique=True)
    
    first_name = models.CharField(max_length=30, blank=False)
    email=models.EmailField(_("email address"), unique=True,blank=False,null=False)
    is_email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone_number"]
    obj=UserManager()
    