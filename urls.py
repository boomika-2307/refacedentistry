from django.urls import path
from . import views
from django.urls import path
from .views import dashboard_stats


urlpatterns = [
    path('', views.home, name='home'),
    path("dashboard-stats/", dashboard_stats),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('doctors/', views.doctors, name='doctors'),
]
