from flask_testing import LiveServerTestCase
from app import app
from selenium import webdriver
import time

class TestParcoursUtilisateur(LiveServerTestCase): 
    def create_app(self): 
        app.config.from_object("configfortests")
        return app
    
    def setUp(self): 
        self.driver = webdriver.Chrome('app/tests/chromedriver.exe')
    
    def tearDown(self):
        self.driver.quit()

    def is_it_the_right_url(self):
        self.driver.get("localhost:8943") # "localhost:8943" ou self.get_server_url(), une méthode de flask testing
        assert self.driver.current_url == "http://127.0.0.1:8943/" or self.driver.current_url == "http://localhost:8943/"

    def test_if_bonjour_path_works(self) : 
        self.is_it_the_right_url() 
        
        self.text_area = self.driver.find_element_by_name('textarea')
        self.text_area.send_keys('bonjour') 
        self.text_area.submit() 

        self.text_element = self.driver.find_element_by_tag_name("body")
        assert self.text_element.text == "bonjour" 

    def test_if_error_path_works(self) : 
        self.is_it_the_right_url() 
        
        self.text_area = self.driver.find_element_by_name('textarea')
        self.text_area.send_keys('hein') 
        self.text_area.submit() 

        self.text_element = self.driver.find_element_by_tag_name("body")
        assert self.text_element.text == "je ne comprends pas"