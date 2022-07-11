import json
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers, viewsets, generics
from rest_framework.response import Response
from map.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
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


class NoteSerializer(serializers.ModelSerializer):
    site = SiteSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'message', 'created_at', 'user', 'site')


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all()
        site_id = self.request.query_params.get('site_id', None)
        if site_id is not None:
            queryset = queryset.filter(site_id=site_id)

        return queryset

    def create(self, request, *args, **kwargs):
        instance = Note.objects.create(message=request.data.get('message'),
                                          user=request.user)
        instance.save()

        topic_id = request.data.get('topic')
        if topic_id:
            topic = Topic.objects.get(id=topic_id)
            topic.notes.add(instance)
            topic.save()

        return Response(NoteSerializer(instance).data)


class TopicSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'description', 'status', 'notes')


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        queryset = Topic.objects.all()

        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'title', 'email', 'phone')


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
