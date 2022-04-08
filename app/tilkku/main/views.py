from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import *
from map.serializers import *


@login_required
def home(request):
    context = {
        'map_servers': serialize('json', MapServer.objects.all()),
        'layers': LayerSerializer(Layer.objects.all(), many=True).data,
    }
    return render(request, 'front.html', context)
