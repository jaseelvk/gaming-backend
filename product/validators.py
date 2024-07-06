# custom_fields.py

from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_image_or_svg(file):
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class CustomImageField(models.FileField):
    default_validators = [validate_image_or_svg]
