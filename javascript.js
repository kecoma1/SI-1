function checkFields() {
    for (i = 0; i < arguments.length; i++) {
        if (document.getElementById(arguments[i]).value.length == 0) {
            alert("Debe introducir información en todos los campos ");
            break;
        }
    }
}

function loadJSON(callback) {
    var obj = new XMLHttpRequest();
    obj.open('GET', 'catalogo.json', true);
    obj.onreadystatechange = function() {
        if (obj.readyState == 4 && obj.status == "200") {
            callback(obj.responseText)
        }
    }
    obj.send(null)
}

function jsonToTable() {
    loadJSON(function())
}

function passwordStrenth() {

}