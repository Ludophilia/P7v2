var site_brand = document.getElementById("site_brand");
var chat_input = document.getElementById("chat_input");
var form = document.querySelector("form");
var chat_zone = document.getElementById("chat_zone");
var container_fluid = document.querySelector(".container-fluid");
var body = document.querySelector("body");
var count_you = 0;
var count_gp = -1;

function ajaxTest(method, target, value, callback) {
    var request = new XMLHttpRequest(); 
    request.open(method, target);
    request.addEventListener("load", function(){
        
        var response = request.responseText; // C'est ici qu'on doit gérer le json, pour le moment, c'est du texte
        
        // console.log(`Ce qui a été envoyé PAR le client : ${value} était de type ${typeof value} d'un point de vue JS`);
        // console.log(`La réponse renvoyée PAR Flask (via return) [${response}] (et traitée par JS avec .responseText) est de type ${typeof response}`);
        
        callback(response); 
        
        // Pas de gestion des erreurs ? 
    });
    request.send(value);
}; 

site_brand.addEventListener("click", function (e) {
    chat_zone.insertAdjacentHTML("beforeend",`<p> <strong>GrandPy</strong> : Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!</p>`); //Rajouter un compteur de clicks, et rajouter des phrases en fonction de l'état du compteur
    e.preventDefault() ;
});

form.addEventListener("submit", function (e) {
    
    var message_val = chat_input.value;
    
    // Affiche le message de l'utilisateur

    chat_zone.insertAdjacentHTML("beforeend", `<p class='message'> <strong>Vous</strong> : <span> </span> </p>`); 
    chat_zone.querySelector(".message:last-child span").setAttribute("id", `${count_you}`);
    document.getElementById(`${count_you}`).textContent += message_val;
    
    // Affiche le message de grandpy. 

    ajaxTest("POST", "/test", message_val, function (response) { //
        
        var gp_json = JSON.parse(response); // Il suffit de définir une variable qui acceuille la réponse

        // Message texte GrandPy

        console.log(gp_json)

        chat_zone.insertAdjacentHTML("beforeend", `<p class='message'> <strong>GrandPy</strong> : <span> </span> </p>`);
        chat_zone.querySelector(".message:last-child span").setAttribute("id", `${count_gp}`);
        document.getElementById(`${count_gp}`).textContent += gp_json.gp_message;
        count_gp--;
        
        // Carte Gmaps. Ajouter "if qqch" hein, sinon ça s'affiche pour tous les messages
        
        if (gp_json.pi_location.lat !== null) {
            
            // La zone de map doit être construite et disponible 
            
            chat_zone.insertAdjacentHTML("beforeend", `<div id="map" style="height:300px; width:100%; border: 1px solid"> </div>`); // Modif style pour la rendre visible et confirmer son existence
            
            // Initialise_map (fonction callback) doit être construite et rendue disponible 
                        
            // var map;

            var lat = gp_json.pi_location.lat;
            var lng = gp_json.pi_location.lng;
            console.log(lat); 
            console.log(lng); 
            
            function initMap() {
                var map = new google.maps.Map(document.getElementById('map'), {
                center: {'lat': lat, 'lng': lng},
                zoom: 15})
                var marker = new google.maps.Marker({position: {lat: lat, lng: lng}, map: map});
                console.log("initmap executé"); // Ajouté pour voir si le script s'executé
            }

            //Script Google Maps doit être construit
            
            // console.log("avant création script gm");
            // body.insertAdjacentHTML("beforeend", "<script></script>");
            // var script_tag = body.querySelector("script:last-child");
            // script_tag.setAttribute("type","text/javascript");
            // script_tag.setAttribute("src","https://maps.googleapis.com/maps/api/js?key=AIzaSyCPPvSl0BPOq5XNZWrEZ7mu9vnnB73Pgm4&callback=initMap");
            // script_tag.setAttribute("async");
            // console.log("après création script gm");

            // Initialise_map est executé via le callback du script

            initMap(); // Without that, the map won't start
            console.log("initmap lancé");
            };
        });
    
    count_you++;
    chat_input.value = ""; 
    e.preventDefault();
});