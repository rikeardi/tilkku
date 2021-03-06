import json
from datetime import datetime
from itertools import chain

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, viewsets, mixins, generics, status
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
        instance = request.user
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


class UserAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser')


class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            instance = self.get_object()
            instance.username = request.data.get('username')
            instance.first_name = request.data.get('first_name')
            instance.last_name = request.data.get('last_name')
            instance.email = request.data.get('email')
            instance.is_superuser = request.data.get('is_superuser')
            instance.save()

            password = request.data.get('password')
            password2 = request.data.get('password2')
            if password and password2 and password == password2:
                instance.set_password(password)
                instance.save()

            return Response(UserSerializer(instance).data)
        else:
            return Response(status=403)

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            password = request.data.get('password')
            password2 = request.data.get('password2')
            if password is None or password2 is None or password != password2:
                return Response({'error': 'Passwords do not match'})

            instance = User.objects.create(
                username=request.data.get('username'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                email=request.data.get('email'),
                is_superuser=request.data.get('is_superuser'),
                password=password
            )

            return Response(UserSerializer(instance).data)
        else:
            return Response(status=403)


class MapStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapStyle
        fields = ('id', 'name', 'stroke', 'fill', 'opacity', 'stroke_width', 'min_zoom', 'max_zoom', 'font_size')


class MapStyleViewSet(viewsets.ModelViewSet):
    queryset = MapStyle.objects.all()
    serializer_class = MapStyleSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get('name')
        instance.stroke = request.data.get('stroke')
        instance.fill = request.data.get('fill')
        instance.opacity = request.data.get('opacity')
        instance.stroke_width = request.data.get('stroke_width')
        instance.min_zoom = request.data.get('min_zoom')
        instance.max_zoom = request.data.get('max_zoom')
        instance.font_size = request.data.get('font_size')
        instance.save()
        return Response(MapStyleSerializer(instance).data)

    def create(self, request, *args, **kwargs):
        instance = MapStyle.objects.create(name=request.data.get('name'),
                                           stroke=request.data.get('stroke'),
                                           fill=request.data.get('fill'),
                                           opacity=request.data.get('opacity'),
                                           stroke_width=request.data.get('stroke_width'),
                                           min_zoom=request.data.get('min_zoom'),
                                           max_zoom=request.data.get('max_zoom'),
                                           font_size=request.data.get('font_size'))
        return Response(MapStyleSerializer(instance).data)


class LayerSerializer(serializers.ModelSerializer):
    style = MapStyleSerializer(read_only=True)

    class Meta:
        model = Layer
        fields = ('id', 'name', 'style')


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get('name')
        instance.style = MapStyle.objects.get(pk=request.data.get('style'))
        instance.save()
        return Response(LayerSerializer(instance).data)


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
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'area', 'marker', 'description', 'contacts')


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
        instance = Site.objects.create(name=request.data.get('name'))

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        if instance.area:
            instance.area.delete()
        if instance.marker:
            instance.marker.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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


class GeoJSONViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        features = request.data.get('features')
        if features is not None:
            for feature in features:
                if feature.get('type') == 'Feature':
                    properties = feature.get('properties')
                    if properties.get('id'):
                        if feature.get('geometry').get('type') == 'Polygon':
                            area = Area.objects.get(id=properties.get('id'))
                            area.coordinates = feature.get('geometry').get('coordinates')[0]
                            area.save()
                        elif feature.get('geometry').get('type') == 'Point':
                            marker = Marker.objects.get(id=properties.get('id'))
                            marker.coordinates = feature.get('geometry').get('coordinates')
                            marker.save()
                    else:
                        if properties.get('layer_id'):
                            layer = Layer.objects.get(id=properties.get('layer_id'))
                        elif properties.get('layer'):
                            layer = Layer.objects.get(name=properties.get('layer'))
                        else:
                            layer = Layer.objects.get(name='default')

                        if feature.get('geometry').get('type') == 'Polygon':
                            area = Area.objects.create(name=properties.get('name'),
                                                       layer_id=layer.id,
                                                       coordinates=feature.get('geometry').get('coordinates')[0])
                            area.save()
                        elif feature.get('geometry').get('type') == 'Point':
                            marker = Marker.objects.create(name=properties.get('name'),
                                                           layer_id=layer.id,
                                                           coordinates=feature.get('geometry').get('coordinates'))
                            marker.save()

        return Response(GeoJSONSerializer(instance).data)

    def get_object(self):
        return GeoJSON()


class MapServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapServer
        fields = ('id', 'name', 'url', 'attribution')


class MapServerViewSet(viewsets.ModelViewSet):
    queryset = MapServer.objects.all()
    serializer_class = MapServerSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get('name')
        instance.url = request.data.get('url')
        instance.attribution = request.data.get('attribution')
        instance.save()
        return Response(MapServerSerializer(instance).data)

    def create(self, request, *args, **kwargs):
        instance = MapServer.objects.create(name=request.data.get('name'),
                                            url=request.data.get('url'),
                                            attribution=request.data.get('attribution'))
        instance.save()
        return Response(MapServerSerializer(instance).data)
