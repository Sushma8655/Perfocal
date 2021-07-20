from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
app_name = 'maintenance'

urlpatterns = [
    path('', views.home, name='home'),
    path('registryrecords',views.registryrecords,name='registryrecords'),
    path('acknowledge',views.acknowledge,name='acknowledge'),
    # path('acknowledge/<str:elementID>/', views.ackApproved),
    path('maintainClose',views.maintainClose,name='maintainClose'),
    path('repairmaintenance',views.repairmaintenance,name='repairmaintenance'),
    path('recordHistory', views.recordHistory, name='recordHistory'),
    ]