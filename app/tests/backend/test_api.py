import pytest

from app.tests.backend.testtools import TestTools
from app.grandpy.skills import APIManager

@pytest.mark.gpapi #31/07/20 - OK
class TestApiDataReception(TestTools):

    @pytest.mark.gpapi1
    def test_if_get_maps_info_retrieves_the_expected_data(self):
        
        get_address = lambda maps_data: maps_data["results"][0]["formatted_address"].replace(", France", "") 
        maps_data = APIManager().get_location_data("maps")

        assert get_address(maps_data) == "7 Cité Paradis, 75010 Paris"
    
    @pytest.mark.gpapi2
    def test_if_get_wiki_info_retrieves_the_expected_data(self):

        extract_anecdocte = lambda wiki_data: wiki_data["query"]["pages"][0]["extract"].split('\n')[-1]
        extract_title = lambda wiki_data: wiki_data["query"]["pages"][0]["title"]

        expected_anecdocte = "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
        expected_title = "Cité Paradis"

        wiki_data = APIManager().get_location_data("wiki")

        assert extract_anecdocte(wiki_data) == expected_anecdocte
        assert extract_title(wiki_data) == expected_title

    @pytest.mark.gpapi3
    def test_if_get_weather_data_retrieve_the_correct_data(self):

        user_location = {"latitude": "48.896735799681274", "longitude": "2.325297188151602"}

        result = APIManager().get_weather_data(user_location)

        assert type(result) == type(dict())
        assert type(result["tcur"]) == type(int())
        assert type(result["city"]) == type(str())
        assert type(result["description"]) == type(str())
        assert type(result["tmin"]) == type(int())
        assert type(result["tmax"]) == type(int())
        assert type(result["icon"]) == type(str())
