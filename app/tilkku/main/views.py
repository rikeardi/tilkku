from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import MapServer


@login_required
def home(request):
    mapservers = MapServer.objects.all()
    context = {
        "map_servers": serializers.serialize('json', mapservers)
    }
    return render(request, "front.html", context)
