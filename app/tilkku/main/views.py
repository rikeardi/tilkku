from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import *


@login_required
def home(request):
    layers = Layer.objects.select_related()
    areas = Area.objects.select_related()


    context = {
        "map_servers": MapServer.objects.all(),
        "layers": layers,
        "areas": areas,
    }
    return render(request, "front.html", context)
