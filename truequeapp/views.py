from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as django_logout, authenticate, login as django_login
from django.contrib import messages
from truequeapp.models import Publicacion, Usuario

# Create your views here.

def redirect_home(request):
	"""
	Metodo para redigir al home. Usado principalmente para enlazar la pagina de inicio al home
	"""
	return render(request, "truequeapp/home.html")

def home(request):
	return render(request, "truequeapp/home.html")

def contacto(request):
	return render(request, "truequeapp/contacto.html")

def publicaciones(request):
	return render(request, "truequeapp/publicaciones.html")


def login(request):
	if request.method == 'GET':
		return render(request, 'truequeapp/login.html')

	if request.method == "POST":
		nombre_usuario = request.POST['nombre_usuario']
		contraseña = request.POST['contraseña']
		usuario = authenticate(
			username=nombre_usuario, 
			password=contraseña)

		if usuario is not None:
			django_login(request, usuario)
			return HttpResponseRedirect('/home')
		else:
			return HttpResponseRedirect('/registro')

def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/home')

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
		nombre_usuario = request.POST['nombre_usuario']
		rut = request.POST['rut']
		numero = request.POST['numero']
		red_social = request.POST['red_social']
		region = request.POST['region']
		correo = request.POST['correo']
		correo_respaldo = request.POST['correo_respaldo']
		contraseña = request.POST['contraseña']

		#El modelo user ya trae
		usuario = Usuario.objects.create_user(
			username=nombre_usuario, 
			first_name=nombre, 
			last_name=apellido, 
			email=correo, rut=rut, 
			numero=numero, 
			red_social=red_social, 
			region=region, 
			correo_respaldo=correo_respaldo, 
			password=contraseña)

		#redirecciona al indice o home
		return HttpResponseRedirect('/home/')


def publicar_producto(request):
	"""
	Metodo encargado de la publicacion de un producto por parte de un usuario.
	"""
	if request.method == "GET":
		
		return render(request,"truequeapp/publicar.html", {"estados": Publicacion.ESTADOS, "categorias":Publicacion.CATEGORIAS})
	
	if request.method == "POST":

		if request.user.is_authenticated:

			usuario = Usuario.objects.get(id=request.user.id)
			publicacion = Publicacion.objects.create(
				titulo=request.POST["titulo"], 
				descripcion=request.POST["descripcion"], 
				estado=request.POST["estado"],
				categoria=request.POST["categoria"], 
				fotos=request.POST["fotos"], 
				cambio=request.POST["cambio"], 
				publicador=usuario)		
			return render(request, "truequeapp/post_publicar.html")

		else:

			return render(reques, "truequeapp/post_publicar.html")

def test_user(request):
	"""
	Metodo usada para el testeo de diversas funcionalidades de Django, pueden modificarla a conveniencia.
	"""
	if request.method == "GET":

		return render(request,"truequeapp/test_user.html")
	
	if request.method == "POST":

		usuario = request.user
		print(usuario.username)

		return render(request,"truequeapp/test_user.html", {"usuario": usuario})