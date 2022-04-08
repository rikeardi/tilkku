from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from map.models import *
from map.serializers import *


#@login_required
#def home(request):
#    context = {
#        'map_servers': serialize('json', MapServer.objects.all()),
#        'layers': JSONRenderer().render(LayerSerializer(Layer.objects.all(), many=True).data),
#    }
#    return TemplateHTMLRenderer().render(request, 'front.html', context)

class Home(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'front.html'

    @login_required
    def get(self, request, *args, **kwargs):
        context = {
            'map_servers': serialize('json', MapServer.objects.all()),
            'layers': JSONRenderer().render(LayerSerializer(Layer.objects.all(), many=True).data),
        }
        return Response(context, template_name=self.template_name)
