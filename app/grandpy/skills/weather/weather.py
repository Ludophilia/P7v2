from app.grandpy.skills import APIManager #DANGEREUX
from app.grandpy.skills.weather import speech

def tell_weather(user_data, message):

    """Génère un message où GrandPy donne la météo (temperature actuelle, minimale, maximale) 
    en fonction des coordonnées géo de l'utilisateur."""

    user_location = user_data.get("options").get("location")

    if not user_location:
        message += speech.NO_COORDS_GIVEN

    else:
        weather_data = APIManager().get_weather_data(user_location)
        wc_icon = weather_data['icon']

        message += f"<img src='https://openweathermap.org/img/wn/{wc_icon}.png' alt='weather-icon' width='25' height='25'>"
        message += speech.CURRENT_WEATHER(weather_data)
    
    message += "<br>"

    return message 