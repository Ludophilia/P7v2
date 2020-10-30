function getUserPosition() {

    // Permet d'obtenir les coordonnées géographiques de l'utilisateur, moyennant son consentement bien sûr. Utile pour le service météo.

    if (!navigator.geolocation) {
        window.USER_LOCATION = null;
    } else {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                window.USER_LOCATION = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                }
            },
            (error) => {
                window.USER_LOCATION = null;
                console.error(`Erreur code ${error.code}: ${error.message}`);
            }
        );
    };
};

export { getUserPosition };