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
        self.driver.get("localhost:8943")

    def test_what_grandpy_says_when_the_user_clicks_on_the_GrandPy_logo(self):
        self.visit_url()

        self.site_brand = self.driver.find_element_by_id('site_brand')

        self.reactions = {
            0 : "Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!",
            1 : "Mais !?",
            2 : "Ça va !?",
            3 : "Tu peux arrêter ??",
            4 : "C'EST FINI OUI ?",
            5 : "FRANCHEMENT ?",
            7 : "Aucune empathie hein :/",
            9 : "10 fois de suite..."
        }

        for i in range(10): 

            self.action = ActionChains(self.driver)
            self.action.click(self.site_brand).perform()
            time.sleep(2) #Laissez lui le temps de rafraichir le dom, sinon c'est un échec.
            self.text_element = self.driver.find_element_by_css_selector(".message:last-child span")
            
            if i in range(6) or i in [7,9]:
                assert self.text_element.text == self.reactions[i]