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
    path('test/', views.test, name='test'),
    path('publicacion/', views.publicacion_elegida, name='publicacion'),
    path('contactar/', views.contactar, name='contactar'),
    path('trueques_compatibles/', views.trueques_compatibles, name='trueques_compatibles'),
    path('mis_publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    path('mis_trueques/', views.mis_trueques, name='mis_trueques'),
    url(r'^perfil/(?P<username>[a-zA-Z]+[\w\-.]*)/$', views.perfil, name='perfil'),
    path('notificacion/', views.notificacion, name='notificacion'),
    path('oferta_demanda/', views.vista_oferta_demanda, name='oferta_demanda'),
    path('trueque_finalizado/', views.trueque_finalizado, name='trueque_finalizado'),
    path('calificar/', views.calificar, name='calificar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
