from flask_testing import LiveServerTestCase
from app import app
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class TestGrandPyUI(LiveServerTestCase): 
    def create_app(self): 
        app.config.from_object("config_tests")
        return app
    
    def setUp(self): 
        self.driver = webdriver.Chrome('app/tests/chromedriver') #Téléchargez un driver et renseignez son chemin ici
    
    def tearDown(self):
        self.driver.quit()

    def visit_url(self):
        self.driver.get("localhost:8943") # "localhost:8943" ou self.get_server_url(), une méthode de flask testing

    def test_if_it_is_the_right_url(self):
        self.visit_url()
        assert self.driver.current_url == "http://127.0.0.1:8943/" or self.driver.current_url == "http://localhost:8943/"

    def test_if_grandpy_gives_the_adress_and_the_info_related_to_the_adress_and_if_the_map_is_displayed(self):
        self.visit_url()

        self.chat_input = self.driver.find_element_by_id('chat_input')
        self.chat_input.send_keys("Connais-tu l'adresse d'OpenClassrooms") 
        self.chat_input.submit()

        time.sleep(3)

        self.gp_answer = self.driver.find_element_by_css_selector(".message:nth-last-child(3) span")
        self.maps_gmstyle = self.driver.find_element_by_css_selector(".map div div:first-child")
        self.gp_anecdocte = self.driver.find_element_by_css_selector(".message:last-child span")

        assert self.gp_answer.text == "Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris."
        assert self.maps_gmstyle.get_attribute("class") == "gm-style"
        assert self.gp_anecdocte.text == "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. [En savoir plus sur Wikipédia]"