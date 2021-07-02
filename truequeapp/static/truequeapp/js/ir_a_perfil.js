/*JavaScript para ir a alún perfil*/

function irAPerfil(event) {
    regex = /[a-zA-Z]+[\w\-.]*/
    nombre_usuario = document.getElementById("perfil").value;
    if (regex.test(nombre_usuario)) {
        if (event.keyCode === 13) {
        window.location = "/perfil/" + nombre_usuario + "/";
        }
    }
}

function irAPerfilClick(event) {
    regex = /[a-zA-Z]+[\w\-.]*/
    nombre_usuario = document.getElementById("perfil").value;
    if (regex.test(nombre_usuario)) {
        window.location = "/perfil/" + nombre_usuario + "/";
    }
}

function irAPerfilEnlace(event, perfil) {
    regex = /[a-zA-Z]+[\w\-.]*/
    nombre_usuario = perfil;
    if (regex.test(nombre_usuario)) {
        window.location = "/perfil/" + nombre_usuario + "/";
    }
}

function activar() {
    var url = location.href.split("/");
    var navLinks = document.getElementsByTagName("barra-items")[0].getElementsByTagName("li");
    var i = 0;
    var currentPage = url[url.length - 1];
    for (i; i < navLinks.length; i++) {
        var lb = navLinks[i].getElementsByTagName("a").href.split("/");
        if (lb[lb.length - 1] == currentPage) {
            navLinks[i].getElementsByTagName("a").className = "active";
        }
    }
}