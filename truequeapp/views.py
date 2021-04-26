from django.shortcuts import render
from truequeapp.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from truequeapp.models import Publicacion, User

# Create your views here.

def home(request):
	return render(request, "truequeapp/home.html")

def login(request):
	if request.method == 'GET':
		return render(request, 'truequeapp/login.html')

	if request.method == "POST":
		username = request.POST['nick']
		contraseña = request.POST['contraseña']
		user = authenticate(username=username, password=contraseña)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/registro')

def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/')

def home(request):
	return render(request, "truequeapp/home.html")

# La vista de la página de registro
# El método devuelve el template si es requerido por GET
# Si es por POST (mandar info de registro), crea usuario
def registro(request):
	if request.method =='GET':
		return render(request, "truequeapp/registro.html")

	elif request.method == 'POST':
		nombre = request.POST['nombre']
		apellido = request.POST['apellido']
		nick = request.POST['nick']
		rut = request.POST['rut']
		numero = request.POST['numero']
		red_social = request.POST['red_social']
		region = request.POST['region']
		correo = request.POST['correo']
		contraseña = request.POST['contraseña']

		#El modelo user ya tare
		user = User.objects.create_user(username=nick, nombre=nombre, apellido=apellido, 
			correo_respaldo=correo, rut=rut, numero=numero, red_social=red_social, region=region, 
			password=contraseña)

		#redirecciona al indice o home
		return HttpResponseRedirect('/home/')


def publicar_producto(request):

	if request.method == "GET":
		
		return render(request,"truequeapp/publicar.html", {"estados": Publicacion.ESTADOS, "categorias":Publicacion.CATEGORIAS})
	
	if request.method == "POST":

		usuario = User.objects.get(id=3)
		publicacion = Publicacion.objects.create(titulo=request.POST["titulo"], descripcion=request.POST["descripcion"], estado=request.POST["estado"],
								categoria=request.POST["categoria"], fotos=request.POST["fotos"], cambio=request.POST["cambio"], publicador=usuario)		
		return render(request, "truequeapp/post_publicar.html")