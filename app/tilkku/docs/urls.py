from django.urls import path, include
from . import views


urlpatterns = [
    path('<page_name>/', views.page, name='page'),
    path('headers/<id>/delete/', views.header_delete, name='header_delete'),
    path('headers/<id>/', views.header_edit, name='header_edit'),
    path('headers/', views.header_new, name='header_new'),
    path('pages/<id>/delete/', views.page_delete, name='page_delete'),
    path('pages/<id>/', views.page_edit, name='page_edit'),
    path('pages/', views.page_new, name='page_new'),
    path('chapters/<id>/delete/', views.chapter_delete, name='chapter_delete'),
    path('chapters/<id>/', views.chapter_edit, name='chapter_edit'),
    path('chapters/', views.chapter_new, name='chapter_new'),
    path('sections/<id>/delete/', views.section_delete, name='section_delete'),
    path('sections/<id>/', views.section_edit, name='section_edit'),
    path('sections/', views.section_new, name='section_new'),
    path('', views.home, name='home'),
]
