from django.db.models import ImageField
from django.forms import ValidationError


def validate_png(image: ImageField):
    if not image.name.lower().endswith(".png"):
        raise ValidationError("A imagem precisa ser .png")
