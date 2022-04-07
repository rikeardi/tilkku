from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import *


@login_required
def home(request):
    context = {
        'map_servers': serialize('json', MapServer.objects.all()),
        'layers': serialize('json', Layer.objects.prefetch_related('areas').all()),
    }
    return render(request, 'front.html', context)
