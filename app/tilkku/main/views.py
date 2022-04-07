from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from map.models import *


# Create view for the main page
# add login_required decorator to prevent unauthenticated users from accessing the page
# add a context variable to pass list of MapServer objects to the template
# add a context variable to pass list of MapLayer objects to the template with all subobjects (Area, Marker, etc.)
# template: front.html
# name: home
@login_required
def home(request):
    context = {
        'map_servers': serialize('json', MapServer.objects.all()),
        'layers': serialize('json', Layer.objects.all(), fields=('id', 'name', 'area_list', 'marker_list')),
    }
    return render(request, 'front.html', context)
