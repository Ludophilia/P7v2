import sendDataToServer from './modules/ajax.js';
import { makeJson } from './modules/devtools.js';
import { getUserPosition } from './modules/geolocalisation.js';
import { displayMessage, displayMap } from './modules/message.js';
import { selectUserProfile } from './modules/user.js';
import  { adjustInputAreaHeight, adjustWebAppHeight } from './modules/window.js';

//import './style.scss';

function main() {

    // Fonction principale. Met en place les observateurs d'évènement necessaire aux fonctionnalités du site. 

    window.MESSAGE_ID = 0; 
    window.USER_LOCATION = null;

    const user = { username: "user", icon: selectUserProfile() };
    const grandpy = { username: "grandpy", icon: "🤖" };
    const $ = document.querySelector.bind(document);

    let reactions = 0;

    window.addEventListener("orientationchange", adjustWebAppHeight);

    window.addEventListener("resize", adjustWebAppHeight);

    window.addEventListener("load", () => {

        sendDataToServer("GET", "/grandpy/starter/", null, (response) => {
            setTimeout(() => displayMessage(response, grandpy), 0);
        });

        getUserPosition();
    });

    $("#submit_button").addEventListener("click", (e) => {
        
        // Gère ce qui se passe quand on valide le formulaire

        const user_message = $("#input_area").value;
        const is_empty_string = !user_message.trim();
        if (is_empty_string) return e.preventDefault();

        const user_data = makeJson(user_message);

        displayMessage(user_message, user);
        
        sendDataToServer("POST", "/grandpy/chat/", user_data, (response) => {
                    
            const { answer, oc_anecdote, oc_coordinates } = JSON.parse(response);

            displayMessage(answer, grandpy);
            
            if (oc_anecdote && oc_coordinates) {
                displayMap(oc_coordinates, grandpy);
                setTimeout(() => 
                    displayMessage(oc_anecdote, grandpy), 4500
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
        const is_empty_string = !($("#input_area").value.trim());

        if (key_pushed !== 'Enter') return; 
        if (is_empty_string) return;

        $("#submit_button").click();
    });

    $("#brand_logo").addEventListener("click", (e) => {

        // Gère ce qui se passe (la réponse de GrandPy) quand on clique sur le logo du site

        const user_data = JSON.stringify({ reactions: `n${reactions}` })

        sendDataToServer("POST", "/grandpy/wtf/", user_data, (response) => displayMessage(response, grandpy));

        reactions++;
        e.preventDefault();
    });
};

main();