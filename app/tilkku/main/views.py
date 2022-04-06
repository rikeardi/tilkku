from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404

from map.models import MapServer


@login_required
def home(request):
    context = {
        "map_servers": MapServer.objects.all()
    }
    return render(request, "front.html", context)
