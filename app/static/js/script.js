var site_brand = document.getElementById("site_brand");
var chat_input = document.getElementById("chat_input");
var form = document.querySelector("form");
var chat_zone = document.getElementById("chat_zone");
var count_you = 0;
var count_gp = -1;

function ajaxTest(method, target, value, callback) {
    var request = new XMLHttpRequest(); 
    request.open(method, target);
    request.addEventListener("load", function(){
        var response = request.responseText;
        console.log(`Ce qui a été envoyé PAR le client : ${value} était de type ${typeof value} d'un point de vue JS`);
        console.log(`La réponse renvoyée PAR Flask (via return) [${response}] (et traitée par JS avec .responseText) est de type ${typeof response}`);
        callback(response);
    });
    request.send(value);
}; 

site_brand.addEventListener("click", function (e) {
    chat_zone.insertAdjacentHTML("beforeend",`<p> <strong>GrandPy</strong> : Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!</p>`); //Rajouter un compteur de clicks, et rajouter des phrases en fonction de l'état du compteur
    e.preventDefault() ;
});

form.addEventListener("submit", function (e) {
    var message_val = chat_input.value;
    chat_zone.insertAdjacentHTML("beforeend", `<p class='message'> <strong>Vous</strong> : <span> </span> </p>`); 
    chat_zone.querySelector(".message:last-child span").setAttribute("id", `${count_you}`);
    document.getElementById(`${count_you}`).textContent += message_val;
    ajaxTest("POST", "/test", message_val, function (response) { //message_val dans du json
        chat_zone.insertAdjacentHTML("beforeend", `<p class='message'> <strong>GrandPy</strong> : <span> </span> </p>`);
        chat_zone.querySelector(".message:last-child span").setAttribute("id", `${count_gp}`);
        document.getElementById(`${count_gp}`).textContent += response;
        count_gp--;
    });
    count_you++;
    chat_input.value = ""; 
    e.preventDefault();
});