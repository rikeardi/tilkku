from rest_framework import serializers
from .models import *


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ['id', 'name', 'type', 'style', 'areas', 'markers']
