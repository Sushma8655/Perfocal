from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
app_name = 'perfocal'

urlpatterns = [
    path('', views.home, name='home'),
    # path('home/', views.home, name='home'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('machines', views.machines, name="machines"),
    path('MachineInstance', views.MachineInstance, name="MachineInstance"),
    path('production', views.production, name="production"),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    ]