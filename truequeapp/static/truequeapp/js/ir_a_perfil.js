/*JavaScript para ir a alún perfil*/

function irAPerfil(event) {
    regex = /[a-zA-Z0-9_]*[\s\n]+[a-zA-Z0-9_]*/
    nombre_usuario = document.getElementById("perfil").value;
    if (!regex.test(nombre_usuario) && nombre_usuario!=="") {
        if (event.keyCode == 13) {
        window.location = "/perfil/" + nombre_usuario + "/";
        }
    }
}