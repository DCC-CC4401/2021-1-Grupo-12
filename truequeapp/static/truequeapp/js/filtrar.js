/*JavaScript para hacer aparecer el filtro*/

function mostrarFiltro() {
    let filtro = document.getElementById("filtro");
    let text = document.getElementById("titulo_filtro");

    if (filtro.style.display === "flex") {
        filtro.style.display = "none";
        text.style.color = "#2B92E9";
        text.style.textDecorationLine = "underline";
    } else {
        filtro.style.display = "flex";
        text.style.color = "#09477B";
        text.style.textDecorationLine = "none";
    }
}

function marcarTodo(source) {
      let categorias = document.getElementsByName("categoria[]");

      for(let i=0, categoria=categorias.length; i<categoria; i++) {
          categorias[i].checked = source.checked;
      }
}
