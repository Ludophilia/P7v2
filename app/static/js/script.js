var test = document.getElementById("site_brand");
var chat_input = document.getElementById("chat_input");
var form = document.querySelector("form");
var chat_zone = document.getElementById("chat_zone");


test.addEventListener("click", function (e) {
    chat_zone.insertAdjacentHTML("beforeend",`<p> <strong>GrandPy</strong> : Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!</p>`);
    e.preventDefault() ; // empecher la redirection, le rafraichissement de la page

    //Rajouter un compteur de clicks, et rajouter des phrases en fonction de l'état du compteur
});

form.addEventListener("submit", function (e) {
    // Retirer la possibilité d'envoyer des messages vides ? 
    chat_zone.insertAdjacentHTML("beforeend", `<p> <strong>Vous</strong> : ${chat_input.value} </p>`) ;
    chat_input.textContent = "";
    e.preventDefault();
});

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