/*JavaScript publicar.html*/

function addImageButton(i){

    if (i < 6){
        let input_nuevo = document.createElement("input");
        input_nuevo.setAttribute("id","foto_"+i);
        input_nuevo.setAttribute("name","foto_"+i);
        input_nuevo.setAttribute("type","file");
        document.getElementById("input-fotos").appendChild(input_nuevo);
        input_nuevo.insertAdjacentHTML('beforebegin', '<div>');
        input_nuevo.insertAdjacentHTML('afterend', '</div>');

        let agregar_imagen = document.getElementById("agregar-fotos");
        agregar_imagen.setAttribute("onclick","addImageButton("+(i+1)+")");

        if (i == 5){
            let div_foto = document.getElementById("agregar-fotos-div")
            div_foto.style.display = "none";
        }
    }
}