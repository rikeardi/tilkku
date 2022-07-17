from django.contrib.auth.decorators import login_required
from django.urls import path, include
import django.contrib.auth.views
from rest_framework import routers
from django.views.generic import TemplateView

from . import views, forms, api

router = routers.DefaultRouter()
router.register(r'mapstyles', api.MapStyleViewSet)
router.register(r'layers', api.LayerViewSet)
router.register(r'areas', api.AreaViewSet)
router.register(r'markers', api.MarkerViewSet)
router.register(r'sitecategories', api.SiteCategoryViewSet)
router.register(r'sites', api.SiteViewSet)
router.register(r'users', api.UserViewSet)
router.register(r'notes', api.NoteViewSet)
router.register(r'topics', api.TopicViewSet)
router.register(r'contacts', api.ContactViewSet)
router.register(r'geojson', api.GeoJSONViewSet)

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('events/<id>/', views.events, name='events'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/login/', django.contrib.auth.views.LoginView.as_view(authentication_form=forms.LoginForm), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]