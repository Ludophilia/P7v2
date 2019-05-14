var site_brand = document.getElementById("site_brand");
var body = document.querySelector("body");
var container_fluid = document.querySelector(".container-fluid");
var form = document.querySelector("form");
var chat_input = document.getElementById("chat_input");
var chat_zone = document.getElementById("chat_zone");

site_brand.addEventListener("click", function (e) {

    // Gère ce qui se passe (la réponse de GrandPy) quand on clique sur le logo du site 

    chat_zone.insertAdjacentHTML("beforeend",`<p> <strong>GrandPy</strong> : Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!</p>`); 
    e.preventDefault() ;

    //Rajouter un compteur de clicks, et rajouter des phrases en fonction de l'état du compteur
});

function ajaxCommunicate(method, target, value, callback) {
    
    // Envoie les données au serveur et gère ce qu'il se passe quand le serveur renvoie des données  
    
    var request = new XMLHttpRequest(); 
    request.open(method, target);
    request.addEventListener("load", function() {
        var response = request.responseText;
        callback(response);     
        // Pas de gestion des erreurs ? 
    });
    request.send(value);
}; 

function displayMessage(user, message) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy)

    chat_zone.insertAdjacentHTML("beforeend", `<p class='message'> <strong>${user}</strong> : <span> </span> </p>`); 
    chat_zone.querySelector(".message:last-child span").textContent += message;

};

function displayMap(latitude, longitude, zoom_level) {
    
    // En charge d'afficher la carte Google Maps dans la fenêtre de chat

    chat_zone.insertAdjacentHTML("beforeend", `<div class="map" style="height:300px; width:100%; "> </div>`);
                
    function initMap() {
        var map = new google.maps.Map(document.querySelector('.map:last-child'), {
        center: {'lat': latitude, 'lng': longitude},
        zoom: zoom_level})
        var marker = new google.maps.Marker({position: {lat: latitude, lng: longitude}, map: map});
    }

    initMap(); 
};

form.addEventListener("submit", function (e) {
    
    // Gère ce qui se passe quand on valide le formulaire

    var user_message = chat_input.value;

    displayMessage("Vous", user_message);
    
    ajaxCommunicate("POST", "/grandpy", user_message, function (response) {
        
        var gp_json = JSON.parse(response);
        var gp_message = gp_json.gp_message;

        displayMessage("GrandPy", gp_message);
                
        if (gp_json.pi_location.lat !== undefined) {

            var address_lat = gp_json.pi_location.lat;
            var address_lng = gp_json.pi_location.lng;    
                        
            displayMap(address_lat, address_lng, 15);

            };
        });
    
    chat_input.value = ""; 
    e.preventDefault();
});