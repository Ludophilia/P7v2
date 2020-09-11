import pytest

from app.tests.backend.testtools import TestTools
from app.grandpy.skills import Parser

class TestParser:

    @pytest.mark.tprs1
    def test_if_build_stopwords_output_the_expected_stopwords_list(self):

        stopwords_list = Parser()._Parser__stopwords
        samples = ["nous-mêmes", "différentes", "ouverts", "dire", "directe", "absolument", "dit", "dite", "dits",
        "divers", "comme", "suivantes", "ès", "dix-huit", "strictement", "rare", "dixième", "doit", "doivent"]

        assert len(stopwords_list) >= 595 and type(stopwords_list) == type([])
        for sample in samples: assert sample in stopwords_list

    @pytest.mark.tprs2
    def test_if_remove_punctuation_does_remove_punctuation_from_user_input(self):
                
        test_string = Parser()._Parser__remove_punctuation("  Salut??,' {comment} tu ((((((vas) depuis le temps!!, vieille; branche [[[[[velu[e]? ;)            :")
        expected_result = "Salut ? ? comment tu vas depuis le temps ! ! vieille branche velue ?" #On garde les ? ! qui sont significatifs

        assert test_string == expected_result and type(test_string) == type("")

    @pytest.mark.tprs3
    def test_if_extract_keywords_does_extract_keywords_from_user_input(self):
        
        test_string = Parser()._Parser__extract_keywords_from_user_input("Salut, tu connais l'adresse d'oc ?")
        expected_result = "salut\nconnais\nadresse\noc\n?"
        
        assert test_string == expected_result and type(test_string) == type("")
    
    @pytest.mark.tprs4
    def test_if_find_matches_does_extract_keywords_from_user_input(self):

        actual_oc_matches = Parser().find_matches("Salut, Tu connais l'adresse d'oc ?")
        expected_oc_matches = ["know", "oc", "address", "hello"]
        
        for matches in expected_oc_matches:
            assert matches in actual_oc_matches