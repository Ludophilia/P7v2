from flask_testing import LiveServerTestCase
from app import app
from selenium import webdriver
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

    def test_if_grandpy_greets_back(self):
        self.visit_url()

        self.text_area = self.driver.find_element_by_id('chat_input')
        self.text_area.send_keys('bonjour', Keys.ENTER)

        time.sleep(2) #Laissez lui le temps de rafraichir le dom, sinon c'est un échec.

        self.text_element = self.driver.find_element_by_css_selector(".message:last-child span")

        assert self.text_element.text in ["Bonjour!", "Salut!", "Yo!", "Hi!!"]

        #On pourrait aussi s'assurer que GrandPy ne dise pas bonjour dans d'autres situations