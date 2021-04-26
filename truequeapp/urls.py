from django.urls import path
from . import views

urlpatterns = [
	path('home/', views.home, name='home'),
	path('registro', views.registro, name='registro'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name="logout"),
	path('publicar/', views.publicar_producto, name='publicar'),
]