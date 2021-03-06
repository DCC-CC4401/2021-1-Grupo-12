from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout, authenticate, login as django_login
from django.db.models import Avg, Q

from truequeapp.models import Publicacion, Usuario, Trueque, Mensaje, Calificacion


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
        # se cuentan las publicaciones asociadas al usuario cuyo estado se haya completado
        n_publicaciones_activas = len(Publicacion.objects.filter(publicador_id=usuario.id, completado="A").values())

        # se cuentan los trueques con estado abierto donde el usuario es demandante
        n_trueques_a = len(Trueque.objects.filter(estado="A", demandante_id=usuario.id).values())

        # se cuentan los trueques con estado abierto donde el usuario es oferente
        n_trueques_a += len(Trueque.objects.filter(estado="A", oferente_id=usuario.id).values())

        # análogo a lo de arriba pero con trueques concretados
        n_trueques_c = len(Trueque.objects.filter(estado="C", demandante_id=usuario.id).values())
        n_trueques_c += len(Trueque.objects.filter(estado="C", oferente_id=usuario.id).values())

        # Consultar datos de reputacion y obtener el promedio
        reputacion = Calificacion.objects.filter(usuario_id=usuario.id).aggregate(Avg('valor'))
        reputacion_promedio = reputacion["valor__avg"]
        if reputacion_promedio is None:
            reputacion_promedio = "Aún no tienes reputación"

        datos = {"nombre": usuario.first_name, "apellido": usuario.last_name, "usuario": usuario.username,
                 "rut": usuario.rut, "red_social": usuario.red_social, "email": usuario.email,
                 "email_respaldo": usuario.correo_respaldo,
                 "telefono": usuario.numero, "region": usuario.region,
                 "miembro_desde": usuario.date_joined,
                 "n_p_activas": n_publicaciones_activas, "n_t_abiertos": n_trueques_a,
                 "n_t_concretados": n_trueques_c, "reputacion": reputacion_promedio}

        # Generar un mensaje default si es que el usuario no tiene telefono
        telefono = usuario.numero
        if telefono == "":
            telefono = "Aún no haz registrado ningún teléfono"
        datos["telefono"] = telefono

        return render(request, "truequeapp/mi_perfil.html", datos)

    # Si el usuario realizando la request no es el mismo que el username entregado, renderiza el perfil.
    elif request.user.is_authenticated:
        # se cuentan las publicaciones asociadas al usuario cuyo estado se haya completado
        n_publicaciones_activas = len(Publicacion.objects.filter(publicador_id=usuario.id, completado="A").values())

        # se cuentan los trueques con estado abierto donde el usuario es demandante
        n_trueques_a = len(Trueque.objects.filter(estado="A", demandante_id=usuario.id).values())

        # se cuentan los trueques con estado abierto donde el usuario es oferente
        n_trueques_a += len(Trueque.objects.filter(estado="A", oferente_id=usuario.id).values())

        # análogo a lo de arriba pero con trueques concretados
        n_trueques_c = len(Trueque.objects.filter(estado="C", demandante_id=usuario.id).values())
        n_trueques_c += len(Trueque.objects.filter(estado="C", oferente_id=usuario.id).values())

        # Consultar datos de reputacion y obtener el promedio
        reputacion = Calificacion.objects.filter(usuario_id=usuario.id).aggregate(Avg('valor'))
        reputacion_promedio = reputacion["valor__avg"]
        if reputacion_promedio is None:
            reputacion_promedio = "Aún no tiene reputación este usuario"

        datos = {"nombre": usuario.first_name, "apellido": usuario.last_name, "usuario": usuario.username,
                 "email": usuario.email, "region": usuario.region, "miembro_desde": usuario.date_joined,
                 "n_p_activas": n_publicaciones_activas, "n_t_abiertos": n_trueques_a, "n_t_concretados": n_trueques_c,
                 "reputacion": reputacion_promedio}

        # Generar un mensaje default si es que el usuario no tiene redes sociales
        red_social = usuario.red_social
        if red_social == "":
            red_social = "El usuario no ha registrado ninguna red social"
        datos["red_social"] = red_social

        # Generar un mensaje default si es que el usuario no tiene telefono
        telefono = usuario.numero
        if telefono == "":
            telefono = "El usuario no ha registrado ningún teléfono"
        datos["telefono"] = telefono

        datos.update({"publicaciones": Publicacion.objects.filter(publicador_id=usuario.id)})
        return render(request, "truequeapp/perfil.html", datos)

    # Si el usuario realizando la request no ha iniciado sesión, se le redirecciona al la pagina de login.
    else:
        return HttpResponseRedirect('/login/')


# Renderiza las publicaciones del usuario.
def mis_publicaciones(request):
    # Si el usuario realizando la request es el mismo que el username entregado, renderiza su perfil.
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(username=request.user.username)

        # se cuentan las publicaciones asociadas al usuario cuyo estado se haya completado
        n_publicaciones_activas = len(Publicacion.objects.filter(publicador_id=usuario.id, completado="A").values())

        # se cuentan los trueques con estado abierto donde el usuario es demandante
        n_trueques_a = len(Trueque.objects.filter(estado="A", demandante_id=usuario.id).values())

        # se cuentan los trueques con estado abierto donde el usuario es oferente
        n_trueques_a += len(Trueque.objects.filter(estado="A", oferente_id=usuario.id).values())

        # análogo a lo de arriba pero con trueques concretados
        n_trueques_c = len(Trueque.objects.filter(estado="C", demandante_id=usuario.id).values())
        n_trueques_c += len(Trueque.objects.filter(estado="C", oferente_id=usuario.id).values())

        # Consultar datos de reputacion y obtener el promedio
        reputacion = Calificacion.objects.filter(usuario_id=usuario.id).aggregate(Avg('valor'))
        reputacion_promedio = reputacion["valor__avg"]
        if reputacion_promedio is None:
            reputacion_promedio = "Aún no tienes reputación"

        publicaciones_usuario = Publicacion.objects.filter(publicador_id=request.user.id, completado="A")
        datos = {"nombre": usuario.first_name, "apellido": usuario.last_name, "usuario": usuario.username,
                 "rut": usuario.rut, "red_social": usuario.red_social, "email": usuario.email,
                 "email_respaldo": usuario.correo_respaldo,
                 "telefono": usuario.numero, "region": usuario.region,
                 "miembro_desde": usuario.date_joined,
                 "n_p_activas": n_publicaciones_activas, "n_t_abiertos": n_trueques_a,
                 "n_t_concretados": n_trueques_c, "reputacion": reputacion_promedio,
                 "publicaciones": publicaciones_usuario}

        return render(request, "truequeapp/mis_publicaciones.html", datos)

    # Si el usuario realizando la request no ha iniciado sesión, se le redirecciona al la pagina de login.
    else:
        return HttpResponseRedirect('/login/')


def mis_trueques(request):
    # Ve si es que el username entregado existe.
    # noinspection PyBroadException

    # Si el usuario realizando la request es el mismo que el username entregado, renderiza su perfil.
    if request.user.is_authenticated:
        trueques_usuario_of = Trueque.objects.filter(oferente_id=request.user.id)
        trueques_usuario_de = Trueque.objects.filter(demandante_id=request.user.id)
        trueque_como_oferente = []
        trueque_como_demandante = []
        trueques = []

        for trueque in trueques_usuario_of:
            publicacion_oferente = Publicacion.objects.get(id=trueque.publicacion_oferente.id)
            if publicacion_oferente.completado == "A":
                publicacion_oferente_id = publicacion_oferente.id
                publicacion_oferente_foto = publicacion_oferente.foto_principal.url
                publicacion_oferente_titulo = publicacion_oferente.titulo
                publicacion_oferente_estado = publicacion_oferente.get_estado_display
                oferente = Usuario.objects.get(id=trueque.oferente.id).username
                publicacion_demandante = Publicacion.objects.get(id=trueque.publicacion_demandante.id)
                publicacion_demandante_id = publicacion_demandante.id
                publicacion_demandante_foto = publicacion_demandante.foto_principal.url
                publicacion_demandante_titulo = publicacion_demandante.titulo
                publicacion_demandante_estado = publicacion_demandante.get_estado_display
                demandante = Usuario.objects.get(id=trueque.demandante.id).username
                trueque_como_oferente += [{'publicacion_oferente_id': publicacion_oferente_id,
                                           'publicacion_oferente_foto': publicacion_oferente_foto,
                                           'publicacion_oferente_titulo': publicacion_oferente_titulo,
                                           'publicacion_oferente_estado': publicacion_oferente_estado,
                                           'oferente': oferente,
                                           'publicacion_demandante_id': publicacion_demandante_id,
                                           'publicacion_demandante_foto': publicacion_demandante_foto,
                                           'publicacion_demandante_titulo': publicacion_demandante_titulo,
                                           'publicacion_demandante_estado': publicacion_demandante_estado,
                                           'demandante': demandante,
                                           }]

        for trueque in trueques_usuario_de:
            publicacion_oferente = Publicacion.objects.get(id=trueque.publicacion_oferente.id)
            if publicacion_oferente.completado == "A":
                publicacion_oferente_id = publicacion_oferente.id
                publicacion_oferente_foto = publicacion_oferente.foto_principal.url
                publicacion_oferente_titulo = publicacion_oferente.titulo
                publicacion_oferente_estado = publicacion_oferente.get_estado_display
                oferente = Usuario.objects.get(id=trueque.oferente.id).username
                publicacion_demandante = Publicacion.objects.get(id=trueque.publicacion_demandante.id)
                publicacion_demandante_id = publicacion_demandante.id
                publicacion_demandante_foto = publicacion_demandante.foto_principal.url
                publicacion_demandante_titulo = publicacion_demandante.titulo
                publicacion_demandante_estado = publicacion_demandante.get_estado_display
                demandante = Usuario.objects.get(id=trueque.demandante.id).username
                trueque_como_demandante += [{'publicacion_oferente_id': publicacion_oferente_id,
                                             'publicacion_oferente_foto': publicacion_oferente_foto,
                                             'publicacion_oferente_titulo': publicacion_oferente_titulo,
                                             'publicacion_oferente_estado': publicacion_oferente_estado,
                                             'oferente': oferente,
                                             'publicacion_demandante_id': publicacion_demandante_id,
                                             'publicacion_demandante_foto': publicacion_demandante_foto,
                                             'publicacion_demandante_titulo': publicacion_demandante_titulo,
                                             'publicacion_demandante_estado': publicacion_demandante_estado,
                                             'demandante': demandante,
                                             }]

        usuario = Usuario.objects.get(id=request.user.id)

        # se cuentan las publicaciones asociadas al usuario cuyo estado se haya completado
        n_publicaciones_activas = len(Publicacion.objects.filter(publicador_id=usuario.id, completado="A").values())

        # se cuentan los trueques con estado abierto donde el usuario es demandante
        n_trueques_a = len(Trueque.objects.filter(estado="A", demandante_id=usuario.id).values())

        # se cuentan los trueques con estado abierto donde el usuario es oferente
        n_trueques_a += len(Trueque.objects.filter(estado="A", oferente_id=usuario.id).values())

        # análogo a lo de arriba pero con trueques concretados
        n_trueques_c = len(Trueque.objects.filter(estado="C", demandante_id=usuario.id).values())
        n_trueques_c += len(Trueque.objects.filter(estado="C", oferente_id=usuario.id).values())

        # Consultar datos de reputacion y obtener el promedio
        reputacion = Calificacion.objects.filter(usuario_id=usuario.id).aggregate(Avg('valor'))
        reputacion_promedio = reputacion["valor__avg"]
        if reputacion_promedio is None:
            reputacion_promedio = "Aún no tienes reputación"

        datos = {"nombre": usuario.first_name, "apellido": usuario.last_name,
                 "usuario": usuario.username, "rut": usuario.rut,
                 "red_social": usuario.red_social, "email": usuario.email,
                 "email_respaldo": usuario.correo_respaldo, "telefono": usuario.numero,
                 "region": usuario.region, "miembro_desde": usuario.date_joined,
                 "n_p_activas": n_publicaciones_activas, "n_t_abiertos": n_trueques_a,
                 "n_t_concretados": n_trueques_c, "reputacion": reputacion_promedio,
                 'trueque_como_oferente': trueque_como_oferente, 'trueque_como_demandante': trueque_como_demandante}

        return render(request, "truequeapp/mis_trueques.html", datos)

    # Si el usuario realizando la request no ha iniciado sesión, se le redirecciona al la pagina de login.
    else:
        return HttpResponseRedirect('/login/')


# Renderiza las publicaciones.
def publicaciones(request):
    todas_las_categorias = Publicacion.CATEGORIAS
    filtros = request.GET.getlist("categoria[]")

    if len(filtros) == 0:
        publicaciones_totales = Publicacion.objects.all()

    else:
        publicaciones_totales = Publicacion.objects.filter(categoria__in=filtros)

    # generamos una lista con sola las publicaciones actualmente abiertas
    publicaciones_existentes = []
    for publicacion in publicaciones_totales:
        # si es publicacion oferente y esta abierta
        if Trueque.objects.filter(publicacion_oferente_id = publicacion.id).exists():
            if Trueque.objects.get(publicacion_oferente_id = publicacion.id).estado == "A" or \
                Trueque.objects.get(publicacion_oferente_id = publicacion.id).estado == "F":
                publicaciones_existentes += [publicacion]
        # si es publicacion demandante y esta abierta
        elif Trueque.objects.filter(publicacion_demandante_id = publicacion.id).exists():
            if Trueque.objects.get(publicacion_demandante_id = publicacion.id).estado == "A" or \
                Trueque.objects.get(publicacion_demandante_id = publicacion.id).estado == "F":
                publicaciones_existentes += [publicacion]
        # si no esta asociada a ningun trueque, solamente debe estar activa
        else:
        	publicaciones_existentes += [publicacion]
            
    request.path = "/publicaciones/?categorias=filtros'"
    return render(request, "truequeapp/publicaciones.html", {"publicaciones_totales": publicaciones_existentes,
                                                             "categorias": todas_las_categorias})


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
        # publ = TruequesAbiertos.objects.filter(interesado_id=5).first()
        # publ.estado = "C"
        # publ.save(update_fields=["estado"])
        trueque = Trueque.objects.filter(demandante_id=request.user.id).first()
        mensaje = Mensaje.objects.create(usuario=request.user, trueque_asoc=trueque, tipo="C")
        mensaje = Mensaje.objects.create(usuario=request.user, trueque_asoc=trueque, tipo="R")
        mensaje = Mensaje.objects.create(usuario=request.user, trueque_asoc=trueque, tipo="A")

        return render(request, "truequeapp/test.html")
    
    if request.method == "POST":
        foo = Trueque.objects.create(publicacion_demandante=Publicacion.objects.filter(categoria="AF").first(),
                                     demandante=request.user)
        if foo.id:
            return render(request, "truequeapp/test.html", {"foo": foo})
        else:
            return render(request, "truequeapp/contacto_fallido.html", {"foo": foo})


# Renderiza la página de publicacion elegida.
def publicacion_elegida(request):
    publicacion = Publicacion.objects.get(id=request.GET["id"])
    oferente = Usuario.objects.get(id=publicacion.publicador_id)
    num_pub = len(Publicacion.objects.filter(publicador_id=oferente.id))
    pub_act = len(Publicacion.objects.filter(publicador_id=oferente.id, completado="A"))

    # se cuentan los trueques con estado abierto donde el usuario es demandante
    trueque_ab = len(Trueque.objects.filter(estado="A", demandante_id=oferente.id))
    # se cuentan los trueques con estado abierto donde el usuario es oferente
    trueque_ab += len(Trueque.objects.filter(estado="A", oferente_id=oferente.id))

    # análogo a lo de arriba pero con trueques concretados
    trueque_con = len(Trueque.objects.filter(estado="C", demandante_id=oferente.id))
    trueque_con += len(Trueque.objects.filter(estado="C", oferente_id=oferente.id))

    # Consultar datos de reputacion y obtener el promedio
    reputacion = Calificacion.objects.filter(usuario_id=oferente.id).aggregate(Avg('valor'))
    reputacion_promedio = reputacion["valor__avg"]
    if reputacion_promedio is None:
        reputacion_promedio = "Aún no tiene reputación este usuario"

    info_oferente = {
        'username': oferente.username,
        'num_pub': num_pub,
        'pub_act': pub_act,
        'tru_abi': trueque_ab,
        'tru_con': trueque_con,
        'fecha': oferente.date_joined,
        'reputacion': reputacion_promedio
    }
    return render(request, 'truequeapp/publicacion_elegida.html', {"publicacion": publicacion, 'info': info_oferente})


def trueques_compatibles(request):
    if request.user.is_authenticated:
        publicacion_oferente = Publicacion.objects.get(id=request.GET["id_p"])
        demandante = request.user
        publicaciones_compatibles = Publicacion.objects.filter(publicador_id=demandante.id).filter \
            (categoria=publicacion_oferente.cambio)
        if len(publicaciones_compatibles) != 0:
            return render(request, 'truequeapp/trueques_compatibles.html', {"publicaciones_compatibles":
                                                                                publicaciones_compatibles,
                                                                            "publicacion_oferente": publicacion_oferente})
        else:
            return render(request, "truequeapp/contacto_fallido.html",
                          {"perfil_usuario": publicacion_oferente.publicador})
    else:
        return HttpResponseRedirect('/login/')


# por arreglar despues
def contactar(request):
    if request.user.is_authenticated:
        publicacion_oferente = Publicacion.objects.get(id=request.GET["id_o"])
        oferente = Usuario.objects.get(id=publicacion_oferente.publicador.id)

        # en caso de tratar de intercambiar con uno mismo
        if request.user.id == oferente.id:
            return perfil(request, request.user.username)

        demandante = request.user
        publicacion_demandante = Publicacion.objects.get(id=request.GET["id_d"])
        # aqui cambiar demandante por publicacion oferente
        if Trueque.objects.filter(publicacion_oferente_id=publicacion_oferente.id,
                                  publicacion_demandante_id=publicacion_demandante.id,
                                  oferente_id=oferente.id,
                                  demandante_id=demandante.id).exists():
            return render(request, "truequeapp/post_solic_trueque_ya_realizado_oferente.html")
        elif Trueque.objects.filter(publicacion_oferente_id=publicacion_demandante.id,
                                    publicacion_demandante_id=publicacion_oferente.id,
                                    oferente_id=demandante.id,
                                    demandante_id=oferente.id).exists():
            return render(request, "truequeapp/post_solic_trueque_ya_realizado_demandante.html")
        else:
            trueque = Trueque.objects.create(publicacion_oferente=publicacion_oferente, demandante=demandante,
                                             oferente=oferente,
                                             publicacion_demandante=publicacion_demandante)
            Mensaje.objects.create(usuario=oferente, trueque_asoc=trueque, tipo="R")
            return render(request, "truequeapp/post_solic_trueque.html", {"trueque": trueque})
    else:
        return HttpResponseRedirect('/login/')


def vista_oferta_demanda(request):
    mensaje = Mensaje.objects.get(id=request.GET["id_m"])
    trueque = Trueque.objects.get(id=request.GET["id_t"])
    demandante = trueque.demandante
    publicacion_ofrecida = trueque.publicacion_demandante
    publicacion_oferente = trueque.publicacion_oferente
    oferente = trueque.oferente

    usuario = request.user

    # se cuentan las publicaciones asociadas al usuario cuyo estado se haya completado
    n_publicaciones_activas = len(Publicacion.objects.filter(publicador_id=usuario.id, completado="A").values())

    # se cuentan los trueques con estado abierto donde el usuario es demandante
    n_trueques_a = len(Trueque.objects.filter(estado="A", demandante_id=usuario.id).values())

    # se cuentan los trueques con estado abierto donde el usuario es oferente
    n_trueques_a += len(Trueque.objects.filter(estado="A", oferente_id=usuario.id).values())

    # análogo a lo de arriba pero con trueques concretados
    n_trueques_c = len(Trueque.objects.filter(estado="C", demandante_id=usuario.id).values())
    n_trueques_c += len(Trueque.objects.filter(estado="C", oferente_id=usuario.id).values())

    # Consultar datos de reputacion y obtener el promedio
    reputacion = Calificacion.objects.filter(usuario_id=usuario.id).aggregate(Avg('valor'))
    reputacion_promedio = reputacion["valor__avg"]
    if reputacion_promedio is None:
        reputacion_promedio = "Aún no tiene reputación este usuario"

    datos = {"nombre": usuario.first_name, "apellido": usuario.last_name, "usuario": usuario.username,
             "red_social": usuario.red_social, "email": usuario.email,
             "telefono": usuario.numero, "region": usuario.region, "miembro_desde": usuario.date_joined,
             "n_p_activas": n_publicaciones_activas, "n_t_abiertos": n_trueques_a, "n_t_concretados": n_trueques_c,
             "reputacion": reputacion_promedio}
    datos.update({"publicaciones": Publicacion.objects.filter(publicador_id=usuario.id)})
    return render(request, 'truequeapp/vista_oferta_demanda.html', {"ofrecido": publicacion_ofrecida,
                                                                    "oferente": oferente,
                                                                    "demandada": publicacion_oferente,
                                                                    "demandante": demandante, "trueque": trueque,
                                                                    "mensaje": mensaje,
                                                                    "reputacion": reputacion_promedio})


#vista despues de aceptar o rechazar trueque
def trueque_finalizado(request):
    if request.user.is_authenticated:
        aceptado = request.GET["aceptado"]
        trueque = Trueque.objects.get(id=request.GET["id_t"])
        mensaje = Mensaje.objects.get(id=request.GET["id_m"])
        if aceptado == "0":
            # primero, procesamos los mensajes
            mensaje.estado = "V"
            mensaje.save(update_fields=["estado"])
            Mensaje.objects.create(usuario=trueque.demandante, trueque_asoc=trueque, tipo="A")

            # ahora el trueque
            trueque.estado = "F"
            trueque.save(update_fields=["estado"])
            return render(request, 'truequeapp/trueque_finalizado.html', {"mensaje": "Usted ha rechazado el trueque"})

        else:  # aceptado == "1"
            # primero, procesamos los mensajes

            mensaje.estado = "V"
            mensaje.save(update_fields=["estado"])

            Mensaje.objects.create(usuario=trueque.oferente, trueque_asoc=trueque, tipo="C")
            Mensaje.objects.create(usuario=trueque.demandante, trueque_asoc=trueque, tipo="C")

            # ahora el trueque y las publicaciones
            trueque.estado = "C"
            trueque.save(update_fields=["estado"])
            publicacion_ofrecida = trueque.publicacion_demandante
            publicacion_oferente = trueque.publicacion_oferente
            publicacion_ofrecida.completado = "E"
            publicacion_oferente.completado = "E"
            publicacion_ofrecida.save(update_fields=["completado"])
            publicacion_oferente.save(update_fields=["completado"])

            return render(request, 'truequeapp/trueque_finalizado.html', {"mensaje": "Usted ha aceptado el trueque"})

    else:
        return HttpResponseRedirect('/login')

# vista al momento de calificar al otro usuario después de un trueque concretado
def calificar(request):
    trueque = Trueque.objects.get(id=request.GET["id_t"])
    mensaje = Mensaje.objects.get(id=request.GET["id_m"])

    if request.method == "GET":
        return render(request, 'truequeapp/calificar.html', {"trueque": trueque})

    if request.method == "POST":
        mensaje.estado = "V"
        mensaje.save(update_fields=["estado"])
        valor = request.POST["calificacion"]

        if request.user == trueque.demandante:
            Calificacion.objects.create(usuario=trueque.oferente, trueque=trueque, valor=valor)
            return HttpResponseRedirect('/home/')

        else:
            Calificacion.objects.create(usuario=trueque.demandante, trueque=trueque, valor=valor)
            return HttpResponseRedirect('/home/')

    else:
        HttpResponseRedirect('/login')


def notificacion(request):
    if request.user.is_authenticated:

        if "id_m" in request.GET:
            mensaje = Mensaje.objects.get(id=request.GET["id_m"])
            mensaje.estado = "V"
            mensaje.save(update_fields=["estado"])

        mensajes = Mensaje.objects.filter(usuario_id=request.user.id, estado='N')
        mensajes_html = []
        for mensaje in mensajes:
            trueque = Trueque.objects.get(id=mensaje.trueque_asoc_id)
            demandante = Usuario.objects.get(id=trueque.demandante_id)
            oferente = Usuario.objects.get(id=trueque.oferente_id)
            if mensaje.tipo == "C":
                link = f"/calificar?id_t={trueque.id}&id_m={mensaje.id}"
                if demandante.id == request.user.id:
                    informacion = f"Trueque aceptado por {oferente.username}, califica el intercambio"
                else:
                    informacion = f"Haz aceptado el trueque con {demandante.username}, califica el intercambio"
            elif mensaje.tipo == "R":
                link = f"/oferta_demanda?id_t={trueque.id}&id_m={mensaje.id}"
                informacion = f"El usuario {demandante.username} quiere intercambiar un producto contigo, revisalo"

            else:  # tipo = "A"
                link = f"/notificacion?id_m={mensaje.id}"
                informacion = f"Trueque rechazado por {oferente.username}, lo sentimos"
            tipo = mensaje.get_tipo_display()

            mensajes_html += [{'informacion': informacion, 'link': link, 'tipo': tipo}]

        return render(request, "truequeapp/notificacion.html", {"mensajes": mensajes_html})
    else:
        return HttpResponseRedirect('/login/')
