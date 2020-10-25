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
    document.getElementById("sidevalues1").style.opacity = "1";
    document.getElementById("sidevalues2").style.opacity = "1";
    document.getElementById("sidevalues3").style.opacity = "1";
    document.getElementById("sidevalues4").style.opacity = "1";
    document.getElementById("sidevalues5").style.opacity = "1";
    document.getElementById("sidevalues6").style.opacity = "1";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("sidevalues1").style.opacity = "0";
    document.getElementById("sidevalues2").style.opacity = "0";
    document.getElementById("sidevalues3").style.opacity = "0";
    document.getElementById("sidevalues4").style.opacity = "0";
    document.getElementById("sidevalues5").style.opacity = "0";
    document.getElementById("sidevalues6").style.opacity = "0";
    document.body.style.backgroundColor = "white";
}
