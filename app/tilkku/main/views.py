from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import MapServer
from .models import LazyEncoder


@login_required
def home(request):
    context = {
        "map_servers": list(MapServer.objects.all())
    }
    return render(request, "front.html", context)
