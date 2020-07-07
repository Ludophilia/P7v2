function sendDataToServer(method, target_url, data_to_send, callback) {
    
    // Envoie les données au serveur et gère ce qu'il se passe quand le serveur renvoie des données  
    
    const request = new XMLHttpRequest(); 

    request.open(method, target_url);
    request.addEventListener("load", () => {
        try {
            callback(request.responseText);
        } catch (error) {
            console.error(error);
        };
    });
    request.send(data_to_send);
}; 

function focusOnLastMessage() {

    // Permet de toujours afficher à l'écran le dernier message

    $("#dialogue_area").lastElementChild.scrollIntoView(true);
};

async function displayMessage(message_str, { username, icon }, animationDuration=1) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy). 

    MESSAGE_ID +=1;
    const message_id = MESSAGE_ID;

    const message_container_html = `<div class='message_container'>\
    <div class="${username} message" id="message${message_id}">\
    ${username === "grandpy"? message_str : ""}</div>\
    <div class='profile_icon'>${icon}</div></div>`;

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

    const message_id = await displayMessage(map_html, user, animationDuration);

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

function ajustInputAreaHeight() {

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

function main() {

    $ = document.querySelector.bind(document); $$ = document.querySelectorAll.bind(document);

    MESSAGE_ID = 0;

    const user = { username: "user", icon: selectUserProfile() };
    const grandpy = { username: "grandpy", icon: "🤖" };

    let reactions = 0;

    window.addEventListener("load", () => {

        // Solution au problème posé par Safari qui ne supporte pas correctement les 100vh comme hauteur

        // $("body").style.height = `${this.innerHeight}px`;

        // DEBUG
        $("#dialogue_area").innerHTML += `<br><span>LOAD window.innerHeight: ${this.innerHeight}px / Height: ${$("body").style.height}</span>`;
        focusOnLastMessage();
    });

    window.addEventListener("orientationchange", () => {

        // Solution au problème posé par Safari qui ne supporte pas correctement les 100vh comme hauteur

        const windowInnerHeight = `${this.innerHeight}px`;

        //if (windowInnerHeight === $("body").style.height) return;

        // $("body").style.height = windowInnerHeight;

        // DEBUG
        $("#dialogue_area").innerHTML += `<br><span>ORIENTATION window.innerHeight: ${this.innerHeight}px</span>`;
        focusOnLastMessage();
    });

    // window.addEventListener("deviceorientation", () => {

    //     // Solution au problème posé par Safari qui ne supporte pas correctement les 100vh comme hauteur

    //     const windowInnerHeight = `${this.innerHeight}px`;

    //     //if (windowInnerHeight === $("body").style.height) return;

    //     // $("body").style.height = windowInnerHeight;

    //     // DEBUG
    //     $("#dialogue_area").innerHTML += `<br><span>DEVICEORIENTATION window.innerHeight: ${this.innerHeight}px</span>`;
    //     focusOnLastMessage();
    // });

    $("body").addEventListener("click", () => {

        // Solution au problème posé par Safari qui ne supporte pas correctement les 100vh comme hauteur

        //const windowInnerHeight = `${this.innerHeight}px`;

        //if (windowInnerHeight === $("body").style.height) return;

        // DEBUG
        $("#dialogue_area").innerHTML += `<br><span>CLICK window.innerHeight: ${window.innerHeight}px</span>`;
        // $("#dialogue_area").innerHTML += `<br><span>CLICK html.innerHeight: ${$("html").innerHeight}px</span>`;
        // $("#dialogue_area").innerHTML += `<br><span>CLICK body.innerHeight: ${$("body").innerHeight}</span>`;

        $("#dialogue_area").innerHTML += `<br><span>CLICK document.documentElement.clientHeight: ${document.documentElement.clientHeight}px</span>`;
        $("#dialogue_area").innerHTML += `<br><span>CLICK html.clientHeight: ${$("html").clientHeight}px</span>`;
        $("#dialogue_area").innerHTML += `<br><span>CLICK body.clientHeight: ${$("body").clientHeight}px</span>`;

        focusOnLastMessage();
    });

    // window.addEventListener("fullscreenchange", () => {

    //     // Solution au problème posé par Safari qui ne supporte pas correctement les 100vh comme hauteur

    //     const windowInnerHeight = `${this.innerHeight}px`;

    //     //if (windowInnerHeight === $("body").style.height) return;

    //     // $("body").style.height = windowInnerHeight;

    //     // DEBUG
    //     $("#dialogue_area").innerHTML += `<br><span>FULLSCREENCHANGE window.innerHeight: ${this.innerHeight}px}</span>`;
    //     focusOnLastMessage();
    // });

    window.addEventListener("resize", () => {

        // Solution au problème posé par Safari qui ne supporte pas correctement les 100vh comme hauteur

        const windowInnerHeight = `${this.innerHeight}px`;

        //if (windowInnerHeight === $("body").style.height) return;

        $("body").style.height = windowInnerHeight;

        // DEBUG
        $("#dialogue_area").innerHTML += `<br><span>RESIZE window.innerHeight: ${windowInnerHeight}px}</span>`;
        focusOnLastMessage();

    });

    $("#submit_button").addEventListener("click", (e) => {
        
        // Gère ce qui se passe quand on valide le formulaire

        const user_message = $("#input_area").value;
        const is_string_empty = !user_message.trim();

        if (is_string_empty) return e.preventDefault();

        displayMessage(user_message, user);

        sendDataToServer("POST", "/grandpy/chat/", user_message, (response) => {
                    
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
        ajustInputAreaHeight();
        e.preventDefault();
    });

    $("#input_area").addEventListener("input", () => {

        // Gère l'adaptation de la taille du formulaire à son contenu
        ajustInputAreaHeight();
    });

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

        sendDataToServer("POST", "/grandpy/wtf/", `n${reactions}`, (response) => displayMessage(response, grandpy));

        reactions++;
        e.preventDefault();
    });

    $("#brand").addEventListener("click", () => {

        // Permet de remonter rapidement le fil de la conversation en appuyant sur le bloc contenant le logo

        $("#dialogue_area").firstElementChild.scrollIntoView(false);

    });
};

main();