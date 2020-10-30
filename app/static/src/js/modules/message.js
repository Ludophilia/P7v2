async function displayMessage(message_str, { username, icon }, { custom_class = "", animationDuration = 1 } = {}) {

    // Est en charge d'afficher le message des participants au chat (utilisateur et GrandPy). 

    window.MESSAGE_ID +=1;
    const message_id = window.MESSAGE_ID;
    const $ = document.querySelector.bind(document);

    const message_container_html = `
        <div class='message_container ${username}_type ${custom_class}'>\
            <div class="${username} message" id="message${message_id}">\
                ${username === "grandpy"? message_str : ""}\
            </div>\
            <div class='profile_icon'>${icon}</div>\
        </div>
    `;

    if (username === "grandpy") {

        $("#dialogue_area").insertAdjacentHTML(
            "beforeend", 
            `<div class="loading ld ld-square ld-spin" id="animation${message_id}"></div>`
            );
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

function focusOnLastMessage() {

    // Permet de toujours afficher à l'écran le dernier message

    const $ = document.querySelector.bind(document);

    $("#dialogue_area").lastElementChild.scrollIntoView(true);
};

async function displayMap(location, user, animationDuration=1) {

    // Permet d'initialiser la google maps, de l'ajouter au DOM et ainsi de l'afficher.
    
    const $ = document.querySelector.bind(document);

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

export { displayMessage, displayMap, focusOnLastMessage };