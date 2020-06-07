function ajaxCommunicate(method, target_url, data_to_send, callback) {
    
    // Envoie les données au serveur et gère ce qu'il se passe quand le serveur renvoie des données  
    
    const request = new XMLHttpRequest(); 

    request.open(method, target_url);
    request.addEventListener("load", function() {
        callback(request.responseText); //Pas de gestion des erreurs ? 
    });
    request.send(data_to_send);
}; 

function displayLoadingAnimation() {
    
    // Affiche une animation de chargement

    const dialogue_area = document.getElementById("dialogue_area");

    dialogue_area.insertAdjacentHTML("beforeend",`<div class="loading ld ld-square ld-spin" style=”display:block”></div>`);
};

function removeLoadingAnimations() {

    // Retire toutes les animations de chargement

    const dialogue_area = document.getElementById("dialogue_area");
    const loading_animations = dialogue_area.querySelectorAll(".ld-square");

    if (!loading_animations) return;

    loading_animations.forEach((animation) => {
        if (animation.style.display !== "none") animation.style.display = "none";
    });
};

function focusOnLastMessage() {

    // Permet de toujours afficher à l'écran le dernier message

    const my_container = document.querySelector(".my_container");
    const dialogue_area = document.getElementById("dialogue_area");
    const targeted_block = {block: "start", inline: "nearest"};

    dialogue_area.lastElementChild.scrollIntoView(targeted_block);
    my_container.scrollIntoView(targeted_block);
};

function displayMessage(user, message_data, timeout, user_profile_icon = null) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy)

    const dialogue_area = document.getElementById("dialogue_area");
    const profile_icon = user_profile_icon || "🤖"

    window.setTimeout(function() {

        if (user === "grandpy") removeLoadingAnimations();

        // Génère conteneur message
        dialogue_area.insertAdjacentHTML("beforeend", "<div class='message_container'></div>");
        const last_message_container = document.querySelector(".message_container:last-child");

        // Structure le conteneur message
        last_message_container.insertAdjacentHTML("afterbegin", `<div class="${user} message"></div>`);
        last_message_container.insertAdjacentHTML("beforeend", `<div class='profile_icon'>${profile_icon}</div>`);
        
        // Cible la balise contenant le texte
        const last_message_zone = last_message_container.querySelector(".message");
    
        // Ajoute le message dans la balise contenant le texte avec gestion de l'anecdocte 
        const message = message_data.anecdocte || message_data;
        const wiki_url = message_data.wiki_url || null;

        last_message_zone.innerText = message;
        if (!! wiki_url) last_message_zone.insertAdjacentHTML("beforeend", wiki_url);
       
        if (user === "user") displayLoadingAnimation();
        focusOnLastMessage();

    }, 1000*timeout);
};

function displayMap(latitude, longitude, zoom_level, timeout) {
    
    // En charge d'afficher la carte Google Maps dans la fenêtre de chat

    const dialogue_area = document.getElementById("dialogue_area");
    displayLoadingAnimation();

    window.setTimeout(function() {
       
        removeLoadingAnimations()
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

function selectUserProfile() {
    
    // Attribue à l'utilisateur une icone de profil. Version intermédiaire, l'idée finale c'est que l'utilisateur puisse choisir son icone de profil.

    const profile_icons = ["👩", "👤", "👨", "😎", "😱", "🥵", "🥶", "🧐", "🤑"];
    const random_position = Math.floor(Math.random()*(profile_icons.length));
    
    return profile_icons[random_position];
};

function main() {

    const site_brand = document.querySelector("#brand");
    const form = document.querySelector("form");
    const input_area = document.getElementById("input_area");
    const random_user_profile_icon = selectUserProfile(); // A améliorer
    let reactions = 0;

    form.addEventListener("submit", function(e) {
        
        // Gère ce qui se passe quand on valide le formulaire

        const user_message = input_area.value;
        const is_string_empty = !user_message.trim();

        if (is_string_empty) return e.preventDefault();

        displayMessage("user", user_message, 0, random_user_profile_icon);
        ajaxCommunicate("POST", "/grandpy/chat/", user_message, function(response) {
            
            const grandpy_response = JSON.parse(response);
        
            displayMessage("grandpy", grandpy_response.message, 1);
            
            // PROBLEME : message de displayMessage() n'est pas d'un type constant, parfois str, parfois object. COMMENT ON GERE ?

            if (!grandpy_response.location) return;

            displayMap(grandpy_response.location.lat, grandpy_response.location.lng, 15, 1);

            // PROBLEME : Les animations sont vraiment gérées de façon chaotique, pas un meilleur moyen ?

            displayLoadingAnimation();
            displayMessage("grandpy", grandpy_response.anecdocte_and_url, 1);
        });
        
        input_area.value = ""; 
        e.preventDefault();
    });

    form.addEventListener("keyup", function(e) {

        // Gère l'envoi du formulaire en cas d'appui sur la touche entrée

        const user_message = input_area.value;
        const key_pushed = e.code;
        const is_string_empty = !user_message.trim();

        if (key_pushed !== 'Enter') return; 
        if (is_string_empty) return;

        document.querySelector("#submit_button").click();
        
    });

    site_brand.addEventListener("click", function(e) {

        // Gère ce qui se passe (la réponse de GrandPy) quand on clique sur le logo du site

        displayLoadingAnimation();

        ajaxCommunicate("POST", "/grandpy/wtf/", `n${reactions}`, (response) => displayMessage("grandpy", response, 1)
        );

        reactions++;
        focusOnLastMessage();
        e.preventDefault() ;

    });
}

main();