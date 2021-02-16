import pytest

from app.tests.backend.testtools import TestTools
from app.grandpy.skills.tourist_guide.tourist_guide import TouristGuide

@pytest.mark.trgd
class TestTouristGuide:

    OC_EXPECTED_ANECODTE = "L'Hôtel Bourrienne (appelé aussi Hôtel de Bourrienne et "\
    "Petit Hôtel Bourrienne) est un hôtel particulier du XVIIIe siècle situé au 58 "\
    "rue d'Hauteville dans le 10e arrondissement de Paris. Propriété privée, il est "\
    "classé au titre des monuments historiques depuis le 20 juin 1927. En juillet 2015, "\
    "il est acheté par l'entrepreneur Charles Beigbeder pour en faire le siège de ses "\
    "activités d'investissement. [En savoir plus sur <a href='https://fr.wikipedia.org/"\
    "wiki/Hôtel_Bourrienne' target='_blank'>Wikipédia</a>]<br>"
    SPECIAL_STARTER = "Mais t'ai-je déjà raconté l'histoire de ce quartier "\
    "qui m'a vu en culottes courtes ?"
    NO_ANECDOTE = "Désolé, je n'ai pas d'anecdote sur ce lieu! Wikip... "\
    "JE ne sais pas tout non plus ! 😅"
        
    @pytest.mark.trgd1a
    def test_if_get_anecdote_from_coordinates_works_as_expected(self):
        
        ex_oc_coordinates = { "lat" : 48.8748465, "lng" : 2.3504873 }
        matches = []

        actual_anecdote = TouristGuide("").get_anecdote(ex_oc_coordinates, matches)

        assert actual_anecdote == TestTouristGuide.OC_EXPECTED_ANECODTE

    @pytest.mark.trgd1b
    def test_if_get_anecdote_from_coordinates_works_as_expected_when_oc_is_in_matches(self):
        
        ex_oc_coordinates = { "lat" : 48.8748465, "lng" : 2.3504873 }
        matches = ["oc"]

        actual_anecdote = TouristGuide("").get_anecdote(ex_oc_coordinates, matches)
        special_response = f"{TestTouristGuide.SPECIAL_STARTER} " + \
                           TestTouristGuide.OC_EXPECTED_ANECODTE
                           
        assert actual_anecdote == special_response
    
    @pytest.mark.trgd1c
    def test_if_get_anecdote_from_coordinates_works_as_expected_when_encoutering_error(self):
        
        ex_oc_coordinates = { "lat" : 0, "lng" : 2.3504873 }
        matches = ["oc"] # 

        actual_anecdote = TouristGuide("").get_anecdote(ex_oc_coordinates, matches)
                           
        assert actual_anecdote == TestTouristGuide.NO_ANECDOTE

    @pytest.mark.trgd3a
    def test_if_get_address_retrieves_the_correct_address_of_the_point_of_interest(self):

        actual_message = TouristGuide("").get_address("sacré coeur", "") #redondant

        expected_message = "Bien sûr mon poussin ! La voici : \"35 Rue du Chevalier de "\
            "la Barre, 75018 Paris\". <br> Et voilà une carte pour t'aider en plus !!<br>"

        assert actual_message == expected_message

    @pytest.mark.trgd3b
    def test_if_get_address_reacts_to_an_error_accordingly(self):

        actual_message = TouristGuide("").get_address("enfer je sais pas moi", "") #redondant

        expected_message = "Désolé, je n'ai pas d'adresse pour ce lieu... 😞"

        assert actual_message == expected_message

        