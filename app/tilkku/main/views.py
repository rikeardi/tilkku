from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import *


@login_required
def home(request):
    layerlist = Layer.objects.all()
    layers = []
    for layer in layerlist:
        layer.style = MapStyle.objects.get(id=layer.style_id)
        layer.areas = Area.objects.filter(layer=layer.id)
        layers.append(layer)

    context = {
        "map_servers": serialize("json", MapServer.objects.all()),
        "layers": serialize("json", layers),
    }
    return render(request, "front.html", context)
