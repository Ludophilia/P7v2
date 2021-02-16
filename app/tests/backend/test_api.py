import pytest

from app.tests.backend.testtools import TestTools
from app.grandpy.skills import APIManager

@pytest.mark.api #31/07/20 - OK. Ça aurait bien besoin de CICD ici.
class TestApiDataReception(TestTools):

    @pytest.mark.api1a
    def test_if_get_maps_data_retrieves_the_expected_data(self):
        
        maps_data = APIManager().get_maps_data("sacré coeur")
        status = maps_data["status"]

        if status == "OK":
            address = maps_data["candidates"][0]["formatted_address"]
            coordinates = maps_data["candidates"][0]["geometry"]["location"]
            point_of_interest = maps_data["candidates"][0]["name"]

            assert type(maps_data) == type({})
            assert "75018 Paris" in address
            assert 'lat' in coordinates and 'lng' in coordinates and type(coordinates) == type({})
            assert point_of_interest == "Sacré-Cœur"
        
        else:
            raise AssertionError

    @pytest.mark.api1b
    def test_if_get_maps_data_reacts_correctly_to_a_bad_request(self):
        
        maps_data = APIManager().get_maps_data("enfer je sais pas moi")

        assert maps_data is None

    @pytest.mark.api2a
    def test_if_get_closest_wiki_page_retrieves_the_expected_data(self):

        ex_oc_coordinates = { "lat" : 48.8748465, "lng" : 2.3504873 }
        closest_wiki_page = APIManager()._APIManager__get_closest_wiki_page(ex_oc_coordinates)

        assert closest_wiki_page == "Hôtel Bourrienne" # Ça va sans doute changer

    @pytest.mark.api2b
    def test_if_get_closest_wiki_page_reacts_correctly_to_a_bad_request(self):

        ex_oc_coordinates = { "lat" : 0, "lng" : 2.3504873 }
        closest_wiki_page = APIManager()._APIManager__get_closest_wiki_page(ex_oc_coordinates)

        assert closest_wiki_page == None # Ça va sans doute changer

    @pytest.mark.api3a
    def test_if_get_wiki_info_retrieves_the_expected_data(self):

        ex_oc_coordinates = { "lat" : 48.8748465, "lng" : 2.3504873 }
        wiki_data = APIManager().get_wiki_data(ex_oc_coordinates)

        actual_anecdocte = wiki_data["query"]["pages"][0]["extract"]
        actual_title = wiki_data["query"]["pages"][0]["title"]

        expected_anecdocte = "L'Hôtel Bourrienne (appelé aussi Hôtel de Bourrienne et Petit Hôtel "\
            "Bourrienne) est un hôtel particulier du XVIIIe siècle situé au 58 rue d'Hauteville dans "\
            "le 10e arrondissement de Paris. Propriété privée, il est classé au titre des monuments "\
            "historiques depuis le 20 juin 1927. En juillet 2015, il est acheté par l'entrepreneur "\
            "Charles Beigbeder pour en faire le siège de ses activités d'investissement."
        expected_title = "Hôtel Bourrienne"

        assert actual_anecdocte == expected_anecdocte
        assert actual_title == expected_title

    @pytest.mark.api3b
    def test_if_get_wiki_info_reacts_correctly_to_a_bad_request(self):

        ex_oc_coordinates = { "lat" : 0, "lng" : 2.3504873 }
        wiki_data = APIManager().get_wiki_data(ex_oc_coordinates)

        assert wiki_data == None # Ça va sans doute changer

    @pytest.mark.api4
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
