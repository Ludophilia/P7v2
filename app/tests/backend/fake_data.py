"""Fake data for test_answers.py"""

OW_CURRENT_F = {
    "weather": [{
        "description": "couvert",
        "icon": "04d"
    }],
    "main": {
        "temp": 21.94,
        "feels_like": 18.89,
        "temp_min": 21,
        "temp_max": 24.44,
        "humidity": 40
    },
    "name": "Paris"            
}

OW_DAILY_F = {
    "daily": [
        {"temp": {
            "min": 21,
            "max": 24.44,
        }}
    ]
}
GM_API_RESPONSE = {
    "html_attributions": [],
    "results": [
        {
            "formatted_address": "7 Cité Paradis, 75010 Paris, France",
            "geometry": {
                "location": {
                    "lat": 48.8747265,
                    "lng": 2.3505517
                }
            },
            "name": "Openclassrooms",
        }
    ]
}

WM_API_RESPONSE = {
    "query": {
        "pages": [
            {
                "title": "Cité Paradis",
                "extract": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris.\n\n\nSituation et accès\nLa cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
            }
        ]
    }
}