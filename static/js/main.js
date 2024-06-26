import { cambiarEstadoMenu } from "./componentes/menuBurger.js";

// ********** Menú oculto para celu **********
// Menú hamburguesa
let menuBurger = document.querySelector('.menuBurger');
let menuPpal = document.querySelector('#menuPpal');

menuBurger.addEventListener('click', evento => cambiarEstadoMenu(menuPpal, menuBurger));