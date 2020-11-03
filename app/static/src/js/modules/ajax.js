function sendDataToServer(method, target_url, data_to_send, callback) {
    
    // Envoie les données au serveur et gère ce qu'il se passe quand le serveur renvoie des données. J'aurais pu utiliser l'API Fetch, mais laissons comme ça... à l'ancienne.
    
    const request = new XMLHttpRequest();

    request.open(method, target_url);
    request.addEventListener("load", () => {
        try {
            callback(request.responseText);
        } catch(error) {
            console.error(error);
        };
    });
    request.addEventListener("error", (error) => {
        console.error(`Erreur: ${error}`);
    });
    request.send(data_to_send);
}; 

export default sendDataToServer;
