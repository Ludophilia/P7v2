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
        self.driver = webdriver.Chrome('app/tests/chromedriver')
    
    def tearDown(self):
        self.driver.quit()

    def visit_url(self):
        self.driver.get("localhost:8943") # "localhost:8943" ou self.get_server_url(), une méthode de flask testing

    def test_if_it_is_the_right_url(self):
        self.visit_url()
        assert self.driver.current_url == "http://127.0.0.1:8943/" or self.driver.current_url == "http://localhost:8943/"
        
    def test_if_the_message_is_sent_when_the_user_hits_enter(self):
        self.visit_url()

        self.text_area = self.driver.find_element_by_id('chat_input')
        self.text_area.send_keys('bonjour', Keys.ENTER)

        time.sleep(2) #Laissez lui le temps de rafraichir le dom, sinon c'est un échec.

        self.text_element = self.driver.find_element_by_css_selector(".message:last-child span")

        assert self.text_element.text in ["Bonjour!", "Salut!", "Yo!", "Hi!!"]

    def test_if_the_loading_animation_is_displayed(self):
        self.visit_url()

        self.chat_input = self.driver.find_element_by_id('chat_input')
        self.chat_input.send_keys('bonjour', Keys.ENTER)

        self.loading_animation = self.driver.find_element_by_css_selector(".ld:last-child")
        assert self.loading_animation.is_displayed()

        self.chat_input.send_keys("Connais-tu l'adresse d'OpenClassrooms", Keys.ENTER)

        self.loading_animation = self.driver.find_element_by_css_selector(".ld:last-child")
        assert self.loading_animation.is_displayed()

    def test_if_the_last_message_is_always_displayed_to_the_user(self):
        self.visit_url()

        self.chat_input = self.driver.find_element_by_id('chat_input')

        for _ in range(4):
            self.chat_input.send_keys('bonjour', Keys.ENTER)
            self.chat_input.send_keys('Que veut dire notre président quand il affirme que Sisyphe a toujours cet intraduisible à faire rouler', Keys.ENTER)
            self.chat_input.send_keys('Es-tu un premier de cordée ?', Keys.ENTER)
            self.chat_input.send_keys("Connais-tu l'adresse d'OC ?", Keys.ENTER)

        time.sleep(2)

        self.grandpy_answer = self.driver.find_element_by_css_selector(".message:last-child span")

        assert self.grandpy_answer.rect['y'] <= 611 #Ex de rect : {'height': 18, 'width': 61, 'x': 306, 'y': 4051}. Le message est directement visible si les coordonnées sont inférieures à (très très très grossièrement) à 611.
