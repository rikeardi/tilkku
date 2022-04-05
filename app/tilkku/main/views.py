import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import MapServer


@login_required
def home(request):
    context = {
        "map_servers": json.dumps(MapServer.objects.all())
    }
    return render(request, "front.html", context)
