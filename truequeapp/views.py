from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout, authenticate, login as django_login

from truequeapp.models import Publicacion, Usuario, TruequesAbiertos


# Renderiza la pagina de home.
def home(request):
    return render(request, "truequeapp/home.html")


# Renderiza la pagina de contacto.
def contacto(request):
    return render(request, "truequeapp/contacto.html")


# Renderiza la pagina de perfil del usuario si es que el parametro username que recibe y el usuario
# que hizo el request son el mismo, si son distintos y el perfil del usuario que se quiere
# acceder existe, renderiza la pagina del usuario "username". Si el perfil del usuario que se
# quiere acceder no existe, renderiza la pagina de perfil no encontrado. Por último si el usuario que hace
# el request no esta loggeado lo redirecciona a la pagina de login.
def perfil(request, username):
    # Ve si es que el username entregado existe.
    # noinspection PyBroadException
    try:
        usuario = Usuario.objects.get(username=username)

    # Si no existe renderiza que el perfil no se ha encontrado.
    except:
        datos = {"usuario": username}
        return render(request, "truequeapp/perfil_no_encontrado.html", datos)

    # Si el usuario realizando la request es el mismo que el username entregado, renderiza su perfil.
    if request.user.is_authenticated and request.user == usuario:
        datos = {"nombre": usuario.first_name, "apellido": usuario.last_name, "usuario": usuario.username,
                 "rut": usuario.rut, "red_social": usuario.red_social, "email": usuario.email,
                 "telefono": usuario.numero, "region": usuario.region}
        return render(request, "truequeapp/mi_perfil.html", datos)

    # Si el usuario realizando la request no es el mismo que el username entregado, renderiza el perfil.
    elif request.user.is_authenticated:
        datos = {"nombre": usuario.first_name, "apellido": usuario.last_name, "usuario": usuario.username,
                 "red_social": usuario.red_social, "email": usuario.email,
                 "telefono": usuario.numero, "region": usuario.region, "miembro_desde": usuario.date_joined}
        datos.update({"publicaciones": Publicacion.objects.filter(publicador_id=usuario.id).values()})
        return render(request, "truequeapp/perfil.html", datos)

    # Si el usuario realizando la request no ha iniciado sesión, se le redirecciona al la pagina de login.
    else:
        return HttpResponseRedirect('/login/')


# Renderiza las publicaciones del usuario.
def mis_publicaciones(request):
    publicaciones_usuario = Publicacion.objects.filter(publicador_id=request.user.id).values()
    return render(request, "truequeapp/mis_publicaciones.html", {"publicaciones": publicaciones_usuario})


def mis_trueques(request):
    truequesd = {}
    i = 0
    for publicaciones_usuario in Publicacion.objects.filter(publicador_id=request.user.id):
        for trueques in TruequesAbiertos.objects.filter(publicacion=publicaciones_usuario):
            trueque = {"trueque" + str(i): (trueques.interesado.username, publicaciones_usuario)}
            i += 1
            truequesd.update(trueque)
    return render(request, "truequeapp/mis_trueques.html", truequesd)


# Renderiza las publicacines.
def publicaciones(request):
    publicaciones_totales = Publicacion.objects.all()
    return render(request, "truequeapp/publicaciones.html", {"publicaciones_totales": publicaciones_totales})


# Renderiza pagina de login.
# El método devuelve el template si es requerido por GET.
# Si es por POST (mandar info de login), loggea usuario.
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
            return HttpResponseRedirect('/home/')

        else:
            return HttpResponseRedirect('/login/')


# Renderiza pagina de home al hacer logout.
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/home/')


# Renderiza la página de registro.
# El método devuelve el template si es requerido por GET.
# Si es por POST (mandar info de registro), crea usuario.
def registro(request):
    if request.method == 'GET':
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

        if Usuario.objects.filter(username=nombre_usuario).exists():
            return render(request, "truequeapp/registro.html")

        Usuario.objects.create_user(
            username=nombre_usuario,
            first_name=nombre,
            last_name=apellido,
            email=correo, rut=rut,
            numero=numero,
            red_social=red_social,
            region=region,
            correo_respaldo=correo_respaldo,
            password=contraseña)

        usuario = authenticate(
            username=nombre_usuario,
            password=contraseña)

        if usuario is not None:
            django_login(request, usuario)
            return HttpResponseRedirect('/home/')

        return HttpResponseRedirect('/registro/')


# Renderiza la página para publicar productos.
# El método devuelve el template si es requerido por GET.
# Si es por POST (mandar info de publicacion), crea publicacion.
def publicar_producto(request):
    """
    Metodo encargado de la publicacion de un producto por parte de un usuario.
    """
    if request.method == "GET":
        return render(request, "truequeapp/publicar.html", {"estados": Publicacion.ESTADOS,
                                                            "categorias": Publicacion.CATEGORIAS})

    if request.method == "POST":
        if request.user.is_authenticated:
            usuario = Usuario.objects.get(id=request.user.id)
            Publicacion.objects.create(
                titulo=request.POST["titulo"],
                descripcion=request.POST["descripcion"],
                estado=request.POST["estado"],
                categoria=request.POST["categoria"],
                foto_principal=request.FILES.get("foto_1") if request.FILES.get("foto_1") else None,
                foto_2=request.FILES.get("foto_2") if request.FILES.get("foto_2") else None,
                foto_3=request.FILES.get("foto_3") if request.FILES.get("foto_3") else None,
                foto_4=request.FILES.get("foto_4") if request.FILES.get("foto_4") else None,
                foto_5=request.FILES.get("foto_5") if request.FILES.get("foto_5") else None,
                cambio=request.POST["cambio"],
                publicador=usuario)
            return render(request, "truequeapp/post_publicar.html")

        else:
            return render(request, "truequeapp/post_publicar.html")


def test(request):
    """
    Metodo usada para el testeo de diversas funcionalidades de Django, pueden modificarla a conveniencia.
    """
    if request.method == "GET":
        return render(request, "truequeapp/test.html")

    if request.method == "POST":
        foo = TruequesAbiertos.objects.create(publicacion=Publicacion.objects.filter(categoria="AF").first(),
                                              interesado=request.user)
        if foo.id:
            return render(request, "truequeapp/test.html", {"foo": foo})
        else:
            return render(request, "truequeapp/contacto_fallido.html", {"foo": foo})


# Renderiza la página de publicaion elegida.
def publicacion_elegida(request):
    publicacion = Publicacion.objects.get(id=request.GET["id"])
    return render(request, 'truequeapp/publicacion_elegida.html', {"publicacion": publicacion})


def contactar(request):
    if request.user.is_authenticated:
        publicacion = Publicacion.objects.get(id=request.GET["id_p"])
        interesado = request.user
        if not TruequesAbiertos.objects.filter(publicacion=publicacion, interesado=interesado).exists():
            trueque = TruequesAbiertos.objects.create(publicacion=publicacion, interesado=interesado)
        else:
            trueque = TruequesAbiertos.objects.get(publicacion=publicacion, interesado=interesado)
        if trueque.id:  # Si el trueque tiene id, es valido y entrara aqui
            return perfil(request, publicacion.publicador.username)
        else:
            return render(request, "truequeapp/contacto_fallido.html", {"trueque": trueque})

    else:
        return HttpResponseRedirect('/login/')
