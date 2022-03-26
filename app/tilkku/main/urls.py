from django.contrib.auth.decorators import login_required
from django.urls import path, include
import django.contrib.auth.views
from django.views.generic import TemplateView

from . import views, forms

app_name = 'main'
urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='front.html')), name='home'),
]