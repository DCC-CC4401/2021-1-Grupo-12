/*JavaScript publicar.html*/

function addImageButton(i){

    if (i < 6){

        let input_nuevo = document.createElement("input");
        input_nuevo.setAttribute("id","foto_"+i);
        input_nuevo.setAttribute("name","foto_"+i);
        input_nuevo.setAttribute("type","file");
        input_nuevo.setAttribute("required","");
        document.getElementById("input-fotos").appendChild(input_nuevo);
        input_nuevo.insertAdjacentHTML('beforebegin', '<div>');
        input_nuevo.insertAdjacentHTML('afterend', '</div>');

        let agregar_imagen = document.getElementById("agregar-fotos");
        agregar_imagen.setAttribute("onclick","addImageButton("+(i+1)+")");
    }
}