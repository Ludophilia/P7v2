from flask_testing import LiveServerTestCase
from app import app
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time, requests, os, pytest, zipfile

class TestMasterClass(LiveServerTestCase):

    # def get_chromedriver(self):

    #     # https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30
    #     # https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_mac64.zip
    #     # https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_win32.zip

    #     r = requests.get("https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_mac64.zip")

    #     with open("test", "wb") as f:
    #         f.write(r.content)

    #     #will return webdriver.Chrome('app/tests/chromedriver')

    def get_chromedriver(self, os_name): # Remettez le dans sa classe dédiée
        
        # GET CHROMEDRIVER : https://sites.google.com/a/chromium.org/chromedriver/
        
        ext = {"mac": "mac64", "win": "win32"}.get(os_name)
        chromedriver_url = f"https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_{ext}.zip"

        chromedriver_zip = requests.get(chromedriver_url)

        if not os.path.exists("app/tests/chromedriver"):

            with open("app/tests/chromedriver.zip", "wb") as f:
                f.write(chromedriver_zip.content)# THAT REQUEST shit needs to be replaced.
                          
            with zipfile.ZipFile("app/tests/chromedriver.zip", mode="r") as z:
                chromedriver = z.getinfo("chromedriver") #Python 3.8. Use := to assign and return ?
                z.extract(chromedriver, path="app/tests")
            
            os.remove("app/tests/chromedriver.zip")

        return webdriver.Chrome('app/tests/chromedriver')

    def create_app(self): 
        app.config.from_object("config_tests")
        return app
    
    def setUp(self): 
        self.driver = self.get_chromedriver("mac")
    
    def tearDown(self):
        self.driver.quit()

    def visit_url(self):
        self.driver.get("localhost:8943") # "localhost:8943" ou self.get_server_url(), une méthode de flask testing

    def test_if_it_is_the_right_url(self):
        self.visit_url()
        assert self.driver.current_url == "http://127.0.0.1:8943/" or self.driver.current_url == "http://localhost:8943/"

class TestChatFunctionalityAndErgo(TestMasterClass): 

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

class TestGrandPyAnswersFrontEndSide(TestMasterClass): 

    # Tester si l'utilisateur voit bien le message s'afficher (une fois, sur la question "tu connais l'adresse d'oc ?"")

    # @pytest.mark.test0
    # def test_simple_very_simple(self):
    #     self.get_chromedriver("mac")

    @pytest.mark.test0
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

    def test_if_grandpy_greets_back(self):
        self.visit_url()

        self.text_area = self.driver.find_element_by_id('chat_input')
        self.text_area.send_keys('bonjour', Keys.ENTER)

        time.sleep(2) #Laissez lui le temps de rafraichir le dom, sinon c'est un échec.

        self.text_element = self.driver.find_element_by_css_selector(".message:last-child span")

        assert self.text_element.text in ["Bonjour!", "Salut!", "Yo!", "Hi!!"]

        #On pourrait aussi s'assurer que GrandPy ne dise pas bonjour dans d'autres situations

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