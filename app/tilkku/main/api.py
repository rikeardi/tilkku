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


class GeoJSONSerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField()

    def to_representation(self, obj):
        return {
            'type': obj.geom_type,
            'coordinates': obj.coords,
        }


class GeoJSONViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = GeoJSONSerializer

    def get_queryset(self):
        queryset = Area.objects.all()

        area_id = self.request.query_params.get('area', None)
        if area_id is not None:
            queryset = queryset.filter(id=area_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache =