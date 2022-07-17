import json
from datetime import datetime
from itertools import chain

from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, viewsets, mixins, generics
from rest_framework.response import Response
from map.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.first_name = request.data.get('first_name')
        instance.last_name = request.data.get('last_name')
        instance.email = request.data.get('email')
        instance.save()

        password = request.data.get('password')
        password2 = request.data.get('password2')
        if password and password2 and password == password2:
            instance.set_password(password)
            instance.save()

        return Response(UserSerializer(instance).data)


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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'title', 'email', 'phone')


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        queryset = Contact.objects.all()

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        term = self.request.query_params.get('term', None)
        if term is not None:
            queryset = queryset.filter(Q(name__icontains=term) | Q(title__icontains=term) | Q(email__icontains=term) | Q(phone__icontains=term))

        return queryset

    def create(self, request, *args, **kwargs):
        instance = Contact.objects.create(name=request.data.get('name'),
                                          title=request.data.get('title'),
                                          email=request.data.get('email'),
                                          phone=request.data.get('phone'))
        instance.save()
        return Response(ContactSerializer(instance).data)


class SiteSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    marker = MarkerSerializer(read_only=True)
    category = SiteCategorySerializer(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'area', 'marker', 'category', 'description', 'contacts')


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all().order_by('name')
    serializer_class = SiteSerializer

    def get_queryset(self):
        queryset = Site.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        term = self.request.query_params.get('term', None)
        if term is not None:
            queryset = queryset.filter(name__icontains=term)

        area_id = self.request.query_params.get('area', None)
        marker_id = self.request.query_params.get('marker', None)
        if area_id is not None:
            queryset = queryset.filter(area_id=area_id)
        elif marker_id is not None:
            queryset = queryset.filter(marker_id=marker_id)

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        contact = Contact.objects.get(id=request.data.get('contact'))
        instance.contacts.add(contact)

        instance.save()
        return Response(SiteSerializer(instance).data)


class NoteSerializer(serializers.ModelSerializer):
    site = SiteSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    topic = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'message', 'created_at', 'user', 'site', 'topic', 'link')


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all()

        site_id = self.request.query_params.get('site', None)
        if site_id is not None:
            queryset = queryset.filter(site_id=site_id)

        return queryset

    def create(self, request, *args, **kwargs):
        instance = Note.objects.create(message=request.data.get('message'),
                                          user=request.user)
        instance.save()

        link = request.data.get('link')
        if link:
            instance.link = link
            instance.save()

        topic_id = request.data.get('topic')
        if topic_id:
            topic = Topic.objects.get(id=topic_id)
            topic.notes.add(instance)
            topic.save()

        site_id = request.data.get('site')
        if site_id:
            site = Site.objects.get(id=site_id)
            instance.site = site
            instance.save()

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status')
        instance.save()
        return Response(TopicSerializer(instance).data)


class GeoJSONFeatureSerializer(serializers.Serializer):
    type = serializers.CharField()
    properties = serializers.DictField()
    geometry = serializers.DictField()

    def to_representation(self, obj):
        return {
            'type': 'Feature',
            'properties': {
                'stroke': obj.layer.style.stroke,
                'stroke-width': obj.layer.style.stroke_width,
                'stroke-opacity': obj.layer.style.opacity + 0.2,
                'fill': obj.layer.style.fill,
                'fill-opacity': obj.layer.style.opacity,
                'name': obj.name,
                'id': obj.id,
                'layer_id': obj.layer.id,
            },
            'geometry': {
                'type': obj.type,
                'coordinates': obj.coordinates
            },
        }


class GeoJSONSerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField()

    def to_representation(self, obj):
        return {
            'type': 'FeatureCollection',
            'features': GeoJSONFeatureSerializer(obj.features, many=True).data
        }


class GeoJSONViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GeoJSON()
    serializer_class = GeoJSONSerializer

    class Meta:
        model = GeoJSON
        fields = ('type', 'features')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        areas = Area.objects.all()
        markers = Marker.objects.all()

        layers = request.query_params.get('layers', None)
        if layers is not None:
            layers = layers.split(',')
            areas = areas.filter(layer__id__in=layers)
            markers = markers.filter(layer__id__in=layers)

        for area in areas:
            area.type = "Polygon"
            area.coordinates = [area.coordinates]
            instance.features.append(area)

        for marker in markers:
            marker.type = "Point"
            instance.features.append(marker)

        return Response(GeoJSONSerializer(instance).data)

    def get_object(self):
        return GeoJSON()
