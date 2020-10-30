function makeJson(user_message) {

    // Permet de créer un JSON avec différentes options en fonction de l'input utilisateur.

    let options = {};

    if (/heure/gmi.test(user_message)) {
        options.timezone = new Date().getTimezoneOffset()/-60;
    };

    if (/temps/gmi.test(user_message)) {
        options.location = USER_LOCATION;
    };
 
    return JSON.stringify({ user_message: user_message, options: options })
};

export { makeJson };