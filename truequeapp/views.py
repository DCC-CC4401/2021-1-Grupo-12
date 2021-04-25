from django.shortcuts import render
from truequeapp.models import User
from django.http import HttpResponseRedirect

# Create your views here.

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
		return HttpResponseRedirect('/')