function activarCampos() {
    let camposDeshab = document.querySelectorAll('td>input');
    document.querySelector('#guardarCambios').removeAttribute('disabled');
    camposDeshab.forEach(campo => campo.removeAttribute('disabled'));
}

let modificar = document.querySelector('#habilitarCampos');
modificar.addEventListener('click', evento => {
    activarCampos();
    evento.preventDefault();
});

// let guardarCambios = document.querySelector('#guardarCambios');
// let idRegistro = document.querySelector('#idRegistro').value;
// guardarCambios.addEventListener('click', evento => guardarEnDB(idRegistro));