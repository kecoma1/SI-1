function checkFields() {
    for (i = 0; i < arguments.length; i++) {
        if (document.getElementById(arguments[i]).value.length == 0) {
            alert("Debe introducir información en todos los campos ");
            break;
        }
    }
}

function jsonToTable() {
    var catalogo = JSON.parse(catalogo.json);
    catalogo[0];
}
