const site_brand = document.querySelector("#brand");
const my_container = document.querySelector(".my_container");
const form = document.querySelector("form");
const input_area = document.getElementById("input_area");
const dialogue_area = document.getElementById("dialogue_area");
let reactions = 0;

function ajaxCommunicate(method, target, value, callback) {
    
    // Envoie les données au serveur et gère ce qu'il se passe quand le serveur renvoie des données  
    
    let request = new XMLHttpRequest(); 
    request.open(method, target);
    request.addEventListener("load", function() {
        let response = request.responseText;
        callback(response);     
        // Pas de gestion des erreurs ? 
    });
    request.send(value);
}; 

function displayMessage(user, message, timeout) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy)
    
    window.setTimeout(function(){
        
        // Retire toutes les animations de chargement
        let loading_animation = dialogue_area.querySelectorAll(".ld-square");
        
        if (user === "GrandPy" && loading_animation !== null) {
            for (let i = 0; i < loading_animation.length; i++) {
                if (loading_animation[i].style.display !== "none") {
                    loading_animation[i].style.display = "none";
                };
            };
        };

        // Génère conteneur message
        dialogue_area.insertAdjacentHTML("beforeend", "<div class='message_container'></div>");
        let last_message_container = document.querySelector(".message_container:last-child");

        // Structure conteneur message
        if (user === "GrandPy") {
            last_message_container.insertAdjacentHTML("afterbegin", `<div class='grandpy message'></div>`);
            last_message_container.insertAdjacentHTML("beforeend", "<div class='profile_icon'>🤖</div>");

        } else if (user === "Vous") {
            last_message_container.insertAdjacentHTML("afterbegin", `<div class='user message'></div>`);
            last_message_container.insertAdjacentHTML("beforeend", "<div class='profile_icon'>😱</div>");
        }
        
        // Cible la balise message
        let last_message_zone = last_message_container.querySelector(".message");

        // Cas de l'anecdocte
        if (message.anecdocte !== undefined) {
            last_message_zone.textContent = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? " + message.anecdocte;
            last_message_zone.insertAdjacentHTML("beforeend", ` [En savoir plus sur <a href="${message.url}" target="_blank">Wikipédia</a>]`)
        } else { // Cas général
            last_message_zone.textContent += message;
        }
       
        // Affiche une animation de chargement
        if (user === "Vous") { 
            dialogue_area.insertAdjacentHTML("beforeend",`<div class="loading ld ld-square ld-spin" style=”display:block”></div>`);
        };

        // Permet de toujours afficher à l'écran le dernier message
        last_message_zone.scrollIntoView({block: "start", inline: "nearest"});
        my_container.scrollIntoView({block: "start", inline: "nearest"});

    }, 1000*timeout);
};

function displayMap(latitude, longitude, zoom_level, timeout) {
    
    // En charge d'afficher la carte Google Maps dans la fenêtre de chat

    window.setTimeout(function() {
       
        dialogue_area.insertAdjacentHTML("beforeend", `<div class="map" style="height:300px; width:100%; "> </div>`);
                
        function initMap() {
            let map = new google.maps.Map(document.querySelector('.map:last-child'), {
            center: {'lat': latitude, 'lng': longitude},
            zoom: zoom_level})
            let marker = new google.maps.Marker({position: {lat: latitude, lng: longitude}, map: map});
        }
        initMap(); 

    },1000*timeout);
};

form.addEventListener("keyup", function(e) {

    // Gère l'envoi du formulaire en cas d'appui sur la touche entrée

    if (e.code === "Enter") {
        document.querySelector("#submit_button").click()
    }
});

form.addEventListener("submit", function(e) {
    
    // Gère ce qui se passe quand on valide le formulaire

    let user_message = input_area.value;

    displayMessage("Vous", user_message, 0);
    
    ajaxCommunicate("POST", "/grandpy", user_message, function(response) {
        
        let gp_json = JSON.parse(response);
    
        displayMessage("GrandPy", gp_json.gp_message, 1);
                
        if (gp_json.pi_location.lat !== undefined) {

            displayMap(gp_json.pi_location.lat, gp_json.pi_location.lng, 15, 1);
            displayMessage("GrandPy", gp_json.pi_anecdocte, 1);

            };
        });
    
    input_area.value = ""; 
    e.preventDefault();
});

site_brand.addEventListener("click", function (e) {

    // Gère ce qui se passe (la réponse de GrandPy) quand on clique sur le logo du site

    let reaction_message = "...";

    switch (reactions) {
        case 0:
            reaction_message = "Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!";
            break;

        case 1:
            reaction_message = "Mais !?";
            break;

        case 2:
            reaction_message = "Ça va !?";
            break;

        case 3:
            reaction_message = "Tu peux arrêter ??";
            break;

        case 4:
            reaction_message = "C'EST FINI OUI ?";
            break;

        case 5:
            reaction_message = "FRANCHEMENT ?";
            break;

        case 7:
            reaction_message = "Aucune empathie hein :/";
            break;

        case 9:
            reaction_message = "10 fois de suite...";
            break;
                    
    };
    reactions++;

    dialogue_area.insertAdjacentHTML("beforeend",`<div class="loading ld ld-square ld-spin" style=”display:block”></div>`);
    dialogue_area.querySelector(".ld:last-child").scrollIntoView({block: "start", inline: "nearest"});
    my_container.scrollIntoView({block: "start", inline: "nearest"});
    displayMessage("GrandPy", reaction_message, 1);

    e.preventDefault() ;

});