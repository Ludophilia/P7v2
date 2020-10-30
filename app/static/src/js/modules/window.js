import { focusOnLastMessage } from './message.js';

function adjustInputAreaHeight() {

    // Modifie la taille du formulaire et de la fenetre de chat au dessus en fonction du contenu formulaire
    
    const $ = document.querySelector.bind(document);

    const is_mobile_with = $("body").clientWidth <= 970;

    const max_height = is_mobile_with ? 120 : 220;
    const base_height = is_mobile_with ? 50 : 60;

    const scroll_height = $("#input_area").scrollHeight > max_height ? max_height : $("#input_area").scrollHeight;
    const container_height = parseInt(getComputedStyle($("#input_container")).height, 10);
    
    if (scroll_height >= max_height && 
        $("#input_area").value != "" &&
        container_height >= base_height+5) return;
    
    $("#input_container").style.height = 
        $("#input_area").value != ""? 
        `${scroll_height}px`: 
        "var(--input_container_height)";

    $("#dialogue_area").style.height = 
        `calc(100% - ${$("#input_container").style.height})`;

    if ($("#dialogue_area").lastElementChild) focusOnLastMessage();
};

function adjustWebAppHeight() {

    // Solution au problème posé par Safari iOS qui ne supporte pas correctement les 100vh comme hauteur

    const $ = document.querySelector.bind(document);

    const isPortrait = window.innerHeight > window.innerWidth;
    const visibleAreaHeight = isPortrait ? `${this.innerHeight}px` : `${$("html").clientHeight}px`;

    if (visibleAreaHeight === $("body").style.height) return;

    $("body").style.height = visibleAreaHeight;
};

export { adjustInputAreaHeight, adjustWebAppHeight };