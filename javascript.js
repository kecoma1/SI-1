function checkFields() {
    for (i = 0; i < arguments.length; i++) {
        if (document.getElementById(arguments[i]).value.length == 0) {
            alert("Debe introducir información en todos los campos ");
            break;
        }
    }
}

function jsonToTable() {
    fetch('./catalogo.json').then(results => results.json()).then(console.log());
    a = 1;
}

function passwordStrenth() {

}