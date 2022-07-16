from rest_framework import serializers
from .models import *


class MapStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapStyle
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    coordinates = serializers.JSONField()

    class Meta:
        model = Area
        fields = '__all__'


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = '__all__'


class LayerSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True)
    markers = MarkerSerializer(many=True)
    style = MapStyleSerializer()

    class Meta:
        model = Layer
        fields = '__all__'


class MapServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapServer
        fields = '__all__'

class WMSServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WMSServer
        fields = '__all__'
