from flask_testing import LiveServerTestCase
from app import app
from app.grandpy import requests
from selenium import webdriver
import time

class TestGrandPyUI(LiveServerTestCase): 
    def create_app(self): 
        app.config.from_object("config_tests")
        return app
    
    def setUp(self): 
        self.driver = webdriver.Chrome('app/tests/chromedriver.exe')
    
    def tearDown(self):
        self.driver.quit()

    def visit_url(self):
        self.driver.get("localhost:8943") # "localhost:8943" ou self.get_server_url(), une méthode de flask testing

    def test_if_it_is_the_right_url(self):
        self.visit_url()
        assert self.driver.current_url == "http://127.0.0.1:8943/" or self.driver.current_url == "http://localhost:8943/"

    def test_if_grandpy_greets_back(self):
        self.visit_url()

        self.text_area = self.driver.find_element_by_id('chat_input')
        self.text_area.send_keys('bonjour') 
        self.text_area.submit()

        time.sleep(2) #Laissez lui le temps de rafraichir le dom, sinon c'est un échec.

        self.text_element = self.driver.find_element_by_css_selector(".message:last-child span")
        assert self.text_element.text in ["Bonjour!", "Salut!", "Yo!", "Hi!!"]

        #On pourrait aussi s'assurer que GrandPy ne dise pas bonjour dans d'autres situations

    def test_if_grandpy_gives_the_adress(self):
        self.visit_url()

        self.text_area = self.driver.find_element_by_id('chat_input')
        self.text_area.send_keys("Connais-tu l'adresse d'OpenClassrooms") 
        self.text_area.submit()

        time.sleep(2)

        self.text_element = self.driver.find_element_by_css_selector(".message:nth-last-child(2) span")

        assert self.text_element.text == "Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris."

    def test_if_the_map_is_displayed_when_the_user_asks_gp_the_adress(self): #Test à améliorer ?
        self.visit_url()

        self.text_area = self.driver.find_element_by_id('chat_input')
        self.text_area.send_keys("Connais-tu l'adresse d'OpenClassrooms") 
        self.text_area.submit()

        time.sleep(2)

        self.maps_gmstyle = self.driver.find_element_by_css_selector(".map div div:first-child")

        assert self.maps_gmstyle.get_attribute("class") == "gm-style" # On considère que si la carte s'affiche (et c'est le cas si la classe gm-style créée par Google s'affiche), tout est correct. Les coordonnées ont été vérifiées dans un autre test. Bien sûr, des problèmes internes à Google Maps pourraient survenir, mais on est pas censer tester Gmaps ici.