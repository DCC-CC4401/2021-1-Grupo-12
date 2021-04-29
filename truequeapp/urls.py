from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.redirect_home, name=''),
	path('home/', views.home, name='home'),
	path('registro', views.registro, name='registro'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name="logout"),
	path('publicar/', views.publicar_producto, name='publicar'),
	path('contacto/', views.contacto, name='contacto'),
	path('publicaciones/', views.publicaciones, name='publicaciones'),
	path('test_user/', views.test_user, name='test'),
	path('publicacion/', views.publicacion_elegida, name='publicacion'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)