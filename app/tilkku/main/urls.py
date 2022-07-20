from django.contrib.auth.decorators import login_required
from django.urls import path, include
import django.contrib.auth.views
from rest_framework import routers

from . import views, forms, api

router = routers.DefaultRouter()
router.register(r'mapservers', api.MapServerViewSet)
router.register(r'mapstyles', api.MapStyleViewSet)
router.register(r'layers', api.LayerViewSet)
router.register(r'areas', api.AreaViewSet)
router.register(r'markers', api.MarkerViewSet)
router.register(r'sitecategories', api.SiteCategoryViewSet)
router.register(r'sites', api.SiteViewSet)
router.register(r'users', api.UserViewSet)
router.register(r'adm_users', api.UserAdminViewSet, basename='adm_users')
router.register(r'notes', api.NoteViewSet)
router.register(r'topics', api.TopicViewSet)
router.register(r'contacts', api.ContactViewSet)
router.register(r'geojson', api.GeoJSONViewSet, basename='geojson')

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('events/<id>/', views.events, name='events'),
    path('api/', include(router.urls)),
    path('lang/<lang>/', views.set_language, name='set_language'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/login/', django.contrib.auth.views.LoginView.as_view(authentication_form=forms.LoginForm), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]
