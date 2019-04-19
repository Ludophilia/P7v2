var site_brand = document.getElementById("site_brand");
var chat_input = document.getElementById("chat_input");
var form = document.querySelector("form");
var chat_zone = document.getElementById("chat_zone");
var count = 0;

site_brand.addEventListener("click", function (e) {
    chat_zone.insertAdjacentHTML("beforeend",`<p> <strong>GrandPy</strong> : Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!</p>`); //Rajouter un compteur de clicks, et rajouter des phrases en fonction de l'état du compteur
    e.preventDefault() ;
});

form.addEventListener("submit", function (e) {
    
    var message_val = chat_input.value;
    chat_zone.insertAdjacentHTML("beforeend", `<p class='message'> <strong>Vous</strong> : <span> </span> </p>`); // Ah, pou sûr, il ne supporte pas l'attribution d'attributs avec des variables...
    chat_zone.querySelector(".message:last-child span").setAttribute("id", `${count}`);
    document.getElementById(`${count}`).textContent += message_val;
    count++;
    chat_input.value = ""; 
    e.preventDefault();
});

/*

Tests :
e>e<
e>e<eeee> (prob)
e\>e\<eeee\> (prob) C'est coupé parce qu'il le prend pour une balise... avec les <>

*/