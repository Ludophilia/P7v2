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

    const dialogue_area = document.getElementById("dialogue_area");
    dialogue_area.lastElementChild.scrollIntoView(true);
};

async function displayMessage(message_str, { username, icon }, animationDuration=1) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy). 

    MESSAGE_ID +=1;

    const message_id = MESSAGE_ID;
    const dialogue_area = document.getElementById("dialogue_area");

    const message_container_html = `<div class='message_container'>\
    <div class="${username} message" id="message${message_id}">\
    ${username === "grandpy"? message_str : ""}</div>\
    <div class='profile_icon'>${icon}</div></div>`;

    if (username === "grandpy") {
        const animation_html = `<div class="loading ld ld-square ld-spin"\
        id="animation${message_id}"></div>`;
        dialogue_area.insertAdjacentHTML("beforeend", animation_html);
        focusOnLastMessage();

        await new Promise((resolve) => {
            setTimeout(() => {
                const animation = document.querySelector(`#animation${message_id}`); 
                animation.outerHTML = message_container_html;
                resolve();
            }, 1000*animationDuration);
        }); // Pas fan de cette solution, mais connait pas mieux pour le moment.

    } else {
        dialogue_area.insertAdjacentHTML("beforeend", message_container_html);
        const message_block = dialogue_area.querySelector(`#message${message_id}`);
        message_block.innerText = message_str;
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
                document.querySelector(`#message${message_id} .map`), {
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

function main() {

    MESSAGE_ID = 0; 

    const site_brand = document.querySelector("#brand");
    const form = document.querySelector("form");
    const input_area = document.getElementById("input_area");

    const user = {username: "user", icon: selectUserProfile()};
    const grandpy = {username: "grandpy", icon: "🤖"};

    let reactions = 0; 

    form.addEventListener("submit", (e) => {
        
        // Gère ce qui se passe quand on valide le formulaire

        const user_message = input_area.value;
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
        
        input_area.value = ""; 
        e.preventDefault();
    });

    form.addEventListener("keyup", (e) => {

        // Gère l'envoi du formulaire en cas d'appui sur la touche entrée

        const user_message = input_area.value;
        const key_pushed = e.code;
        const is_string_empty = !user_message.trim();

        if (key_pushed !== 'Enter') return; 
        if (is_string_empty) return;

        document.querySelector("#submit_button").click();
        
    });

    site_brand.addEventListener("click", (e) => {

        // Gère ce qui se passe (la réponse de GrandPy) quand on clique sur le logo du site

        sendDataToServer("POST", "/grandpy/wtf/", `n${reactions}`, (response) => displayMessage(response, grandpy));

        reactions++;
        e.preventDefault();
    });
};

main();