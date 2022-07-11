import json
from datetime import datetime

from django.contrib import auth
from django.db.models import Q
from rest_framework import serializers, viewsets, generics
from rest_framework.response import Response
from map.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = 'auth.User'
        fields = ('id', 'first_name', 'last_name', 'email')


class UserViewSet(viewsets.ModelViewSet):
    queryset = auth.get_user_model().objects.all()
    serializer_class = UserSerializer


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

    def create(self, request, *args, **kwargs):
        instance = Site.objects.create(name=request.data.get('name'),
                                       category=SiteCategory.objects.get(pk=request.data.get('category')))

        area_id = request.data.get('area')
        if area_id:
            area = Area.objects.get(id=area_id)
            instance.area = area

        marker_id = request.data.get('marker')
        if marker_id:
            marker = Marker.objects.get(id=marker_id)
            instance.marker = marker

        instance.save()
        return Response(SiteSerializer(instance).data)


class MessageSerializer(serializers.ModelSerializer):
    site = SiteSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'header', 'message', 'created_at', 'user', 'site')


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        site_id = self.request.query_params.get('site_id', None)
        if site_id is not None:
            queryset = queryset.filter(site_id=site_id)

        return queryset

    def create(self, request, *args, **kwargs):
        instance = Message.objects.create(header=request.data.get('header'),
                                          message=request.data.get('message'),
                                          user=request.user,
                                          site=Site.objects.get(id=request.data.get('site')))
        instance.save()
        return Response(MessageSerializer(instance).data)


class TopicSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'description', 'status', 'messages')


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
