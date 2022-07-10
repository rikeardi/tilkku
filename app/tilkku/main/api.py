import json
from datetime import datetime

from django.db.models import Q
from rest_framework import serializers, viewsets, generics
from rest_framework.response import Response
from map.models import *


class MapStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapStyle
        fields = ('id', 'name', 'stroke', 'fill', 'opacity')


class MapStyleViewSet(viewsets.ModelViewSet):
    queryset = MapStyle.objects.all()
    serializer_class = MapStyleSerializer


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ('id', 'name', 'type', 'style')


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer


class AreaSerializer(serializers.ModelSerializer):
    layer = LayerSerializer(read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subtitle', 'layer', 'coordinates')


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all().order_by('name')
    serializer_class = AreaSerializer

    def get_queryset(self):
        queryset = Area.objects.all().order_by('name')

        layer_id = self.request.query_params.get('layer_id', None)
        if layer_id is not None:
            queryset = queryset.filter(layer_id=layer_id)

        layer = self.request.query_params.get('layer', None)
        if layer is not None:
            queryset = queryset.filter(layer__name=layer)

        return queryset


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'name', 'layer', 'coordinates')


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer


class SiteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteCategory
        fields = ('id', 'name')


class SiteCategoryViewSet(viewsets.ModelViewSet):
    queryset = SiteCategory.objects.all()
    serializer_class = SiteCategorySerializer


class SiteSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    marker = MarkerSerializer(read_only=True)
    category = SiteCategorySerializer(read_only=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'area', 'marker', 'category', 'description')


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all().order_by('name')
    serializer_class = SiteSerializer

    def get_queryset(self):
        queryset = Site.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset
