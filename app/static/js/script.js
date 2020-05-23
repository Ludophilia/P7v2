function ajaxCommunicate(method, target, value, callback) {
    
    // Envoie les données au serveur et gère ce qu'il se passe quand le serveur renvoie des données  
    
    const request = new XMLHttpRequest(); 

    request.open(method, target);
    request.addEventListener("load", function() {
        const response = request.responseText;
        callback(response);     
        // try {
        // } catch(error) {
        // };Pas de gestion des erreurs ? 
    });
    request.send(value);
}; 

function displayLoadingAnimation() {
    
    const dialogue_area = document.getElementById("dialogue_area");

    // Affiche une animation de chargement

    dialogue_area.insertAdjacentHTML("beforeend",`<div class="loading ld ld-square ld-spin" style=”display:block”></div>`);
};

function removeLoadingAnimations() {

    // Retire toutes les animations de chargement

    const dialogue_area = document.getElementById("dialogue_area");

    const loading_animations = dialogue_area.querySelectorAll(".ld-square");

    if (!! loading_animations) {
        loading_animations.forEach((animation)=> {
            animation.style.display !== "none" ? animation.style.display = "none" 
            : null ; // Un peu concon comme déclaration... mais c'est pour l'exemple.
        })
    };
};

function focusOnLastMessage() {

    const my_container = document.querySelector(".my_container");
    const dialogue_area = document.getElementById("dialogue_area");

    // Permet de toujours afficher à l'écran le dernier message

    dialogue_area.lastElementChild.scrollIntoView({block: "start", inline: "nearest"});
    my_container.scrollIntoView({block: "start", inline: "nearest"});
};

function displayMessage(user, message, timeout) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy)

    const dialogue_area = document.getElementById("dialogue_area");
    
    window.setTimeout(function() {

        if (user === "GrandPy") {
            removeLoadingAnimations();
        };

        // Génère conteneur message
        dialogue_area.insertAdjacentHTML("beforeend", "<div class='message_container'></div>");
        const last_message_container = document.querySelector(".message_container:last-child");

        // Structure le conteneur message
        if (user === "GrandPy") {
            last_message_container.insertAdjacentHTML("afterbegin", `<div class='grandpy message'></div>`);
            last_message_container.insertAdjacentHTML("beforeend", "<div class='profile_icon'>🤖</div>");

        } else if (user === "Vous") {
            last_message_container.insertAdjacentHTML("afterbegin", `<div class='user message'></div>`);
            last_message_container.insertAdjacentHTML("beforeend", "<div class='profile_icon'>😱</div>");
        }
        
        // Cible la balise contenant le texte
        const last_message_zone = last_message_container.querySelector(".message");

        // Ajoute le message dans la balise contenant le texte
    
        // Cas de l'anecdocte (NON NON NON, EN BACKEND ÇA)
        if (!! message.anecdocte) {
            last_message_zone.textContent = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? " + message.anecdocte;
            last_message_zone.insertAdjacentHTML("beforeend", ` [En savoir plus sur <a href="${message.url}" target="_blank">Wikipédia</a>]`)
        } else { // Cas général
            last_message_zone.textContent += message;
        }
       
        if (user === "Vous") { 
            displayLoadingAnimation();
        };

        focusOnLastMessage();

    }, 1000*timeout);
};

function displayMap(latitude, longitude, zoom_level, timeout) {
    
    // En charge d'afficher la carte Google Maps dans la fenêtre de chat

    const dialogue_area = document.getElementById("dialogue_area");

    window.setTimeout(function() {
       
        dialogue_area.insertAdjacentHTML("beforeend", `<div class="map"></div>`);
                
        function initMap() {
            const map = new google.maps.Map(document.querySelector('.map:last-child'), {
            center: {'lat': latitude, 'lng': longitude},
            zoom: zoom_level})
            const marker = new google.maps.Marker({position: {lat: latitude, lng: longitude}, map: map});
        }
        initMap(); 

    },1000*timeout);
};

function main() {

    const site_brand = document.querySelector("#brand");
    const form = document.querySelector("form");
    const input_area = document.getElementById("input_area");

    form.addEventListener("keyup", function(e) {

        // Gère l'envoi du formulaire en cas d'appui sur la touche entrée

        if (e.code === "Enter") {
            document.querySelector("#submit_button").click();
        }
    });

    form.addEventListener("submit", function(e) {
        
        // Gère ce qui se passe quand on valide le formulaire

        const user_message = input_area.value;

        displayMessage("Vous", user_message, 0);
        
        ajaxCommunicate("POST", "/grandpy", user_message, function(response) {
            
            const gp_json = JSON.parse(response);
        
            displayMessage("GrandPy", gp_json.gp_message, 1);
                    
            if (!! gp_json.pi_location.lat) {

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
        let reactions = 0;

        // Stocker les réponses dans un document à part

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

        displayLoadingAnimation(); // démarre sans message de l'utilisateur donc... Il faut l'animation.
        displayMessage("GrandPy", reaction_message, 1);
        focusOnLastMessage();

        e.preventDefault() ;

    });
}

main();