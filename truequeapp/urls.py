from django.urls import path
from . import views

urlpatterns = [
	path('', views.redirect_home, name=''),
	path('home/', views.home, name='home'),
	path('registro', views.registro, name='registro'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name="logout"),
	path('publicar/', views.publicar_producto, name='publicar'),
	path('contacto/', views.contacto, name='contacto'),
	path('publicaciones/', views.publicaciones, name='publicaciones'),
	path('test_user/', views.test_user, name='test')
]