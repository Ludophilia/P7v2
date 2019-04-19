var test = document.getElementById("site_brand");
var chat_input = document.getElementById("chat_input");
var form = document.querySelector("form");
var chat_zone = document.getElementById("chat_zone");

test.addEventListener("click", function (e) {
    chat_zone.insertAdjacentHTML("beforeend",`<p> <strong>GrandPy</strong> : Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!</p>`); //Rajouter un compteur de clicks, et rajouter des phrases en fonction de l'état du compteur
    e.preventDefault() ; // empecher la redirection, le rafraichissement de la page
});

form.addEventListener("submit", function (e) {
    // Retirer la possibilité d'envoyer des messages vides ? 
    var message = chat_input.value; // Toujours ce problème avec chaines de caractères de type "><dddd>>>>ddd>>" qui se retrouvent tronquées de leurs contenus. | Utilisation d'une var, comme si je ne pouvais pas manipuler 2 fois chat_input.value sans avoir des problèmes
    chat_zone.insertAdjacentHTML("beforeend", `<p class="message"> <strong>Vous</strong> : ${message} </p>`) ;
    chat_input.value = "" ; 
    // chat_zone.insertAdjacentHTML("beforeend", $(".message").html()) ;
    // $(".message:last").toggle();
    // $(".message:last").css("color", "red");
    // $(".message:last").slideDown();
    e.preventDefault();
});


// form.addEventListener("submit", function (e) {
    
//     e.preventDefault();
// });

// form.addEventListener("submit", function (e) {
    
//     var message = $('#chat_input').text();
    
//     $('#chat_zone').append(`<p class="message"> <strong>Vous</strong> : ${message} </p>`);
//     $('#chat_input').text() = "";
    
//     $(".message:last").toggle();
//     $(".message:last").css("color", "red");
//     $(".message:last").slideDown();

// });

// $($("form").on("submit", function(e) {
//     var $message = $('#chat_input').text();
//     $('#chat_zone').append($message);
//     $('#chat_input').text() = "";
//     e.preventDefault();
// }));

// form.addEventListener("submit", function (e) {
//     $(".message:last").toggle().fadeIn(1000);
//     e.preventDefault();
// });

// form.addEventListener("submit", function (e) {
//     $(".message:last").css("color", "red");
//     e.preventDefault();
// });

// fadeIn(2000);

// test.addEventListener("click", function (e) {
//     var chat_zone = document.getElementById("chat_zone");
//     chat_zone.textContent += `Pourquoi tu appuies sur mon ${e.target.textContent}, t'es fou ou quoi, c'est fragile ici !!`;
// });

// chat_input.addEventListener("focus", function () {
//     chat_input.textContent = "Tu peux communiquer en écrivant dans cette zone et en appuyant sur le bouton à droite =>"}); 

// chat_input.addEventListener("blur", function () {
//     chat_input.textContent = "Mais... tu veux pas ???"});

// window.addEventListener(
//     "beforeunload", function (e) {
//         e.returnValue = "heu";
//         return "heu";
// });

// window.addEventListener("load", function (e) {
//     e.preventDefault() ;
//     alert("salut frère !!");
// });

// chat_input.focus();