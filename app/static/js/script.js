function sendDataToServer(method, target_url, data_to_send, callback) {
    
    // Envoie les données au serveur et gère ce qu'il se passe quand le serveur renvoie des données. J'aurais pu utiliser l'API Fetch, mais laissons comme ça... à l'ancienne.
    
    const request = new XMLHttpRequest();

    request.open(method, target_url);
    request.addEventListener("load", () => {
        try {
            callback(request.responseText);
        } catch (error) {
            console.error(error);
        };
    });
    request.addEventListener("error", (error) => {
        console.error(`Erreur: ${error}`);
    });
    request.send(data_to_send);
}; 

function focusOnLastMessage() {

    // Permet de toujours afficher à l'écran le dernier message

    $("#dialogue_area").lastElementChild.scrollIntoView(true);
};

async function displayMessage(message_str, { username, icon }, { custom_class = "", animationDuration = 1 } = {}) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy). 

    MESSAGE_ID +=1;
    const message_id = MESSAGE_ID;

    const message_container_html = `
    <div class='message_container ${username}_type ${custom_class}'>\
        <div class="${username} message" id="message${message_id}">\
            ${username === "grandpy"? message_str : ""}\
        </div>\
        <div class='profile_icon'>${icon}</div>\
    </div>
    `;

    if (username === "grandpy") {
        const animation_html = `<div class="loading ld ld-square ld-spin"\
        id="animation${message_id}"></div>`;

        $("#dialogue_area").insertAdjacentHTML("beforeend", animation_html);
        focusOnLastMessage();

        await new Promise((resolve) => {
            setTimeout(() => {
                $(`#animation${message_id}`).outerHTML = message_container_html;
                resolve();
            }, 1000*animationDuration);
        });

    } else {
        $("#dialogue_area").insertAdjacentHTML("beforeend", message_container_html);
        $(`#message${message_id}`).innerText = message_str;
    };

    focusOnLastMessage();

    return Promise.resolve(message_id);
};

async function displayMap(location, user, animationDuration=1) {
    
    const center_coordinates = location;
    const map_html = `<div class="map"></div>`;
    
    const options = { animationDuration: animationDuration }
    const message_id = await displayMessage(map_html, user, options);

    function initMap() {
        const map = new google.maps.Map(
                $(`#message${message_id} .map`), {
                center: center_coordinates,
                zoom: 19,
                gestureHandling: 'cooperative'
            });
        const marker = new google.maps.Marker({
                position: center_coordinates, 
                map: map
            });
    };
    
    initMap();
};

function selectUserProfile() {
    
    // Attribue à l'utilisateur une icone de profil. Version intermédiaire, l'idée finale c'est que l'utilisateur puisse choisir son icone de profil.

    const profile_icons = ["👩", "👤", "👨", "😎", "😱", "🥵", "🥶", "🧐", "🤑"];
    const random_position = Math.floor(Math.random()*(profile_icons.length));
    
    return profile_icons[random_position];
};

function adjustInputAreaHeight() {

    // Modifie la taille du formulaire et de la fenetre de chat au dessus en fonction du contenu formulaire

    const is_mobile_with = $("body").clientWidth <= 800;

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

    const isPortrait = window.innerHeight > window.innerWidth;
    const visibleAreaHeight = isPortrait ? `${this.innerHeight}px` : `${$("html").clientHeight}px`;

    if (visibleAreaHeight === $("body").style.height) return;

    $("body").style.height = visibleAreaHeight;
};

function getUserPosition() {

    if (!navigator.geolocation) {
        USER_LOCATION = null;
    } else {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                USER_LOCATION = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.latitude
                }
            },
            (error) => {
                USER_LOCATION = null;
                console.error(`Erreur code ${error.code}: ${error.message}`);
            }
        );
    };
};

function make_json(user_message) {

    // Permet de créer un JSON avec différentes options en fonction de l'input utilisateur.

    let options = {};

    if (/[Hh]eure/gm.test(user_message)) {
        options.timezone = new Date().getTimezoneOffset()/-60;
    };

    if (/[Tt]emps/gm.test(user_message)) {
        options.location = USER_LOCATION;
    };

    return JSON.stringify({ user_message: user_message, options: options })
};

function main() {

    $ = document.querySelector.bind(document); $$ = document.querySelectorAll.bind(document);

    MESSAGE_ID = 0; USER_LOCATION = null;

    const user = { username: "user", icon: selectUserProfile() };
    const grandpy = { username: "grandpy", icon: "🤖" };

    let reactions = 0;

    window.addEventListener("orientationchange", adjustWebAppHeight);

    window.addEventListener("resize", adjustWebAppHeight);

    window.addEventListener("load", () => {

        if (window.innerWidth <= 800) {
            sendDataToServer("GET", "/grandpy/footer/", null, (response) => {
                displayMessage(response, grandpy, { custom_class: "footer_message" });
            });
        }

        sendDataToServer("GET", "/grandpy/starter/", null, (response) => {
            setTimeout(() => displayMessage(response, grandpy), 0);
        });

        getUserPosition();
    });

    $("#submit_button").addEventListener("click", (e) => {
        
        // Gère ce qui se passe quand on valide le formulaire

        const user_message = $("#input_area").value;
        const is_string_empty = !user_message.trim();
        if (is_string_empty) return e.preventDefault();

        const user_data = make_json(user_message);

        displayMessage(user_message, user);
        
        sendDataToServer("POST", "/grandpy/chat/", user_data, (response) => {
                    
            const { message, anecdocte, location } = JSON.parse(response);

            displayMessage(message, grandpy);
            
            if (anecdocte && location) {
                displayMap(location, grandpy);
                setTimeout(() => 
                    displayMessage(anecdocte, grandpy), 4500
                );
            };
        });
        
        $("#input_area").value = ""; 
        adjustInputAreaHeight();
        e.preventDefault();
    });

    $("#input_area").addEventListener("input", adjustInputAreaHeight);

    $("#input_area").addEventListener("keyup", (e) => {

        // Gère l'envoi du formulaire en cas d'appui sur la touche entrée

        const key_pushed = e.code;
        const is_string_empty = !($("#input_area").value.trim());

        if (key_pushed !== 'Enter') return; 
        if (is_string_empty) return;

        $("#submit_button").click();
    });

    $("#brand_logo").addEventListener("click", (e) => {

        // Gère ce qui se passe (la réponse de GrandPy) quand on clique sur le logo du site

        const user_data = JSON.stringify({ reactions: `n${reactions}` })

        sendDataToServer("POST", "/grandpy/wtf/", user_data, (response) => displayMessage(response, grandpy));

        reactions++;
        e.preventDefault();
    });

    // $("#brand").addEventListener("click", () => {

    //     // Permet de remonter rapidement le fil de la conversation en appuyant sur le bloc contenant le logo
            // Ajoutez un bouton pour remonter le fil (dans une v3 ?) dans la zone de chat qui apparait dès que l'utilisateur dépasse un certain point

    //     if (!$("#dialogue_area").firstElementChild) return;

    //     $("#dialogue_area").firstElementChild.scrollIntoView(false);

    // });
};

main();