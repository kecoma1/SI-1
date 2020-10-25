function validation() {
    fortaleza = document.getElementById("password_strength_meter").value
    contraseña1 = document.getElementById("password_input").value;
    contraseña2 = document.getElementById("password_input_repeat").value;
    if (contraseña1 != contraseña2 || fortaleza != 4) {
        alert('Las contraseñas no cumple los requisitos o son distintas')
        return false;
    } 
    return true;
}

function openNav() {
    document.getElementById("el1").style.visibility = "visible";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("sidenav").style.visibility = "hidden";
    document.body.style.backgroundColor = "white";
}