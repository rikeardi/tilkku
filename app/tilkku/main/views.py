from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from tilkku.map.models import MapServer


@login_required
def home(request):
    context = {
        "map_servers": MapServer.objects.all()
    }
    return render(request, "front.html", context)
