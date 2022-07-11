import json

from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import *
from map.serializers import *


@login_required
def home(request):
    context = {
        'map_servers': json.dumps(MapServerSerializer(MapServer.objects.all(), many=True).data),
        'layers': json.dumps(LayerSerializer(Layer.objects.all().order_by('id'), many=True).data),
    }
    return render(request, 'front.html', context)

