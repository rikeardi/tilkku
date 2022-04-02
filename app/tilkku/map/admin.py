from django.contrib import admin
from models import *


# Register your models here.
admin.site.register(
    LayerType,
    MapStyle,
    Layer,
    Area,
    Marker,
)