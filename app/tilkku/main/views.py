from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import *


@login_required
def home(request):
    layers = Layer.objects.all()
    for layer in layers:
        layer.style = MapStyle.objects.get(id=layer.style_id)
        layer.areas = Area.objects.filter(layer=layer.id)

    context = {
        "map_servers": serialize("json", MapServer.objects.all()),
        "layers": serialize("json", layers),
    }
    return render(request, "front.html", context)
