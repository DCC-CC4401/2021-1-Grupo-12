from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.home, name=''),
	path('home/', views.home, name='home'),
	path('registro/', views.registro, name='registro'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name="logout"),
	path('publicar/', views.publicar_producto, name='publicar'),
	path('contacto/', views.contacto, name='contacto'),
	path('publicaciones/', views.publicaciones, name='publicaciones'),
	path('test_user/', views.test_user, name='test'),
	path('publicacion/', views.publicacion_elegida, name='publicacion'),
	path('mis_publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
	url(r'^perfil/(?P<username>[\w\-]+)/$', views.perfil, name='perfil'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)