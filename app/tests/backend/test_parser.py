import pytest

from app.tests.backend.testtools import TestTools

class TestParser:

    @pytest.mark.tprs1
    def test_if_build_stopwords_output_the_expected_stopwords_list(self):

        pass
        
        #Implémentation modifiée

        # self.gp = GrandPy()
        # stopwords_list = self.gp.stopwords()
        # samples = ["nous-mêmes", "différentes", "ouverts", "dire", "directe", "absolument", "dit", "dite", "dits",
        # "divers", "comme", "suivantes", "ès", "dix-huit", "strictement", "rare", "dixième", "doit", "doivent"]

        # assert len(stopwords_list) >= 600 and type(stopwords_list) == type([])
        # for sample in samples: assert sample in stopwords_list

    @pytest.mark.tprs2
    def test_if_remove_punctuation_remove_punctuation_from_user_input(self):
        pass
        
        #Implémentation modifiée
        
        # self.gp = GrandPy()

        # test_string = self.gp.extract_keywords("  Salut????!?!,' {comment} tu vas depuis le temps!!!, vieille; branche velue? ;)            ")
        # expected_result = "Salut comment tu vas depuis le temps vieille branche velue"

        # assert test_string == expected_result and type(test_string) == type("")

    @pytest.mark.tprs3
    def test_if_remove_stopwords_remove_stopwords_from_user_input(self):
        pass
        
        # self.gp = GrandPy()
        # test_string = self.gp.extract_keywords("Salut, salut mon gros gros pote! Comment tu vas depuis le temps, vieille branche velue? ;)")
        # # test_string = self.gp.remove_stopwords("Salut tu connais l'adresse d'oc")

        # # expected_result = "Salut comment tu vas depuis le temps vieille branche velue "
        # expected_result =['salut', 'gros', 'pote', 'temps', 'vieille', 'branche', 'velue']
        
        # assert test_string == expected_result and type(test_string) == type([])
        # # assert type(test_string) == type("")
        # # print("DE REMOVE_STOPWORDS", test_string)

    @pytest.mark.tprs4
    def test_what_extract_keywords_do(self):
        pass
        # self.gp = GrandPy()

        # print(self.gp.extract_keywords("tu connais l'adresse d'oc?"))

@pytest.mark.gppr
class TestPatternRecognition(TestTools):
    
    @pytest.mark.gppr1
    def test_what_patterns_is_recognized_when_user_ask_for_the_time(self):

        keywords = "\n".join(["quelle", "heure", "?"])
        matches = self.gp.search_patterns(keywords)
        print(matches)
        
        for item in matches:
            assert item in ["what", "time", "question"]