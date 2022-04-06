from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import MapServer, Layer


@login_required
def home(request):
    context = {
        "map_servers": serialize('json', MapServer.objects.values()),
        "layers": serialize('json', Layer.objects.values())
    }
    return render(request, "front.html", context)
