import time, os

import wget, pytest, zipfile
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions

from app import app
from app.models import db, Robot, State, Memory

class ChromeDvrMgr():

    @classmethod
    def get_chromedriver(cls, os_name, version):

        """ Automatise le téléchargement du chromedriver et le renvoie pour utilisation """
        
        # GET CHROMEDRIVER : https://sites.google.com/a/chromium.org/chromedriver/

        dirname = os.path.dirname(os.path.abspath(__file__))
        build_path = lambda file: os.path.join(dirname, file)

        if not os.path.exists(build_path("chromedriver")):
            
            ext = {"mac": "mac64", "win": "win32"}.get(os_name)
            chromedriver_url = f"http://chromedriver.storage.googleapis.com/{version}/chromedriver_{ext}.zip"

            wget.download(chromedriver_url, build_path("chromedriver.zip"))

            with zipfile.ZipFile(build_path("chromedriver.zip"), mode="r") as z:
                chromedriver = z.getinfo("chromedriver") #Python 3.8. Use := (walrus) to assign and return ?
                z.extract(chromedriver, path=build_path(""))
            
            os.system(f"chmod 755 {build_path('chromedriver')}")
            os.remove(build_path("chromedriver.zip"))

        return webdriver.Chrome(build_path('chromedriver'))

class TestMasterClass(LiveServerTestCase):

    def create_app(self): 
        app.config.from_object("config_tests")
        return app
    
    def setUp(self): 
        db.create_all()
        db.session.add(Robot(id=f"127.0.0.1"))
        db.session.commit()
        self.driver = ChromeDvrMgr.get_chromedriver("mac", "84.0.4147.30")
        self.query_selector = self.driver.find_element_by_css_selector
        self.query_selector_all = self.driver.find_elements_by_css_selector
        self.visit_url()
    
    def tearDown(self):
        db.drop_all()
        self.driver.quit()

    def visit_url(self):
        self.driver.get("localhost:8943") # "localhost:8943" ou self.get_server_url(), une méthode de flask testing

    def test_if_it_is_the_right_url(self):
        self.visit_url()
        assert self.driver.current_url == "http://127.0.0.1:8943/" or self.driver.current_url == "http://localhost:8943/"

    def send_message(self, message, send=True): 
        self.chat_input = self.query_selector('#input_area')
        self.chat_input.send_keys(message)
        if send: self.query_selector("#submit_button").click()

@pytest.mark.gpansfe
class TestGrandPyAnswersFrontEndSide(TestMasterClass):

    @pytest.mark.gpansfe0
    def test_if_grandpys_welcome_message_is_correctly_displayed(self):

        time.sleep(2)
        
        self.message = self.query_selector("#message1")
        self.part_of_expected_answer = "Salut 👋, qu'est-ce que je peux faire pour toi ?\n\nTu peux me demander, dans le formulaire juste en bas avec 'Nouveau message' écrit dedans :"

        assert self.part_of_expected_answer in self.message.text

    @pytest.mark.gpansfe1
    def test_if_grandpy_gives_the_adress_and_the_info_related_to_the_adress_and_if_the_map_is_displayed(self):

        self.send_message("Connais-tu l'adresse d'OpenClassrooms") 

        time.sleep(6)

        self.answer = self.query_selector("#message3")
        self.maps = self.query_selector(".map div.gm-style")
        self.anecdocte = self.query_selector("#message5")

        assert self.answer.text == "Bien sûr mon poussin ! La voici : \"7 Cité Paradis, 75010 Paris\".\nEt voilà une carte pour t'aider en plus !!"
        assert self.maps.is_displayed
        assert "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ?" in self.anecdocte.text

    @pytest.mark.gpansfe2
    def test_if_grandpy_greets_back(self):

        self.chat_input = self.query_selector('#input_area')
        self.chat_input.send_keys('bonjour', Keys.ENTER)

        time.sleep(2)

        self.answer = self.query_selector("#message3")

        assert self.answer.text in ["Bonjour!", "Salut!", "Yo!", "Hi!!", "👋"]

    @pytest.mark.gpansfe3
    def test_if_grandpy_answers_accordingly_when_asked_for_something_out_of_his_current_scope(self):

        self.send_message('Garçon !! Je voudrais un verre d\'hydromel, avec 3 glaçons !')

        time.sleep(2)

        self.answer = self.query_selector("#message3")

        assert self.answer.text == "Désolé, je n'ai pas compris ton message... 😕 Dans une prochaine version peut-être ?"

    @pytest.mark.gpansfe4
    def test_what_grandpy_says_when_the_user_clicks_on_the_GrandPy_logo(self):

        self.brand = self.query_selector("#brand_logo > a")

        self.reactions = {
            0 : "Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!",
            1 : "Mais !?",
            2 : "Ça va !?",
            3 : "Tu peux arrêter ??",
            4 : "C'EST FINI OUI ?",
            5 : "FRANCHEMENT ?",
            7 : "Aucune empathie hein :/",
            9 : "10 fois de suite... OK. T'as gagné.",
            10: "..."
        }

        for i in range(11): 

            self.brand.click()
            time.sleep(2) 
            self.answer = self.query_selector(".grandpy_type:last-child > div")
            
            if i in range(6) or i in [7,10]:
                assert self.answer.text == self.reactions[i]

@pytest.mark.gpux
class TestUserExperience(TestMasterClass): 

    @pytest.mark.gpux1
    def test_if_the_message_is_sent_when_the_user_hits_enter(self):
        self.visit_url()

        self.text_area = self.query_selector('#input_area')
        self.text_area.send_keys('bonjour', Keys.ENTER)

        time.sleep(2)

        self.answer = self.query_selector("#message3")

        assert self.answer.text in ["Bonjour!", "Salut!", "Yo!", "Hi!!", "👋"]

    @pytest.mark.gpux2
    def test_if_the_loading_animation_is_displayed(self):
        
        time.sleep(0.5)
        self.loading_animation1 = self.query_selector("#animation1")
        assert self.loading_animation1.is_displayed()

        time.sleep(2)

        self.send_message("bonjour")
        
        time.sleep(0.5)
        self.loading_animation2 = self.query_selector("#animation3")
        assert self.loading_animation2.is_displayed()

    @pytest.mark.gpux3
    def test_if_the_last_message_is_always_displayed_to_the_user(self):

        self.send_message('Bonjour')
        self.send_message('Au revoir')
        self.send_message('Special Feature')
        self.send_message('Wow')

        time.sleep(2)

        self.answer = self.query_selector(".message_container:last-child")

        assert self.answer.rect['y'] <= 660 #Ex de rect : {'height': 18, 'width': 61, 'x': 306, 'y': 4051}. Le message est directement visible si les coordonnées sont inférieures à (très très très grossièrement) à 611.

    @pytest.mark.gpux4
    def test_if_the_last_message_is_displayed_when_the_user_type_something_in_the_input(self):

        self.send_message('Bonjour')
        self.send_message('Au revoir')
        self.send_message('Special Feature')
        self.send_message('Wow')

        time.sleep(1)

        self.target = self.query_selector("#dialogue_area")

        while self.query_selector("#message1").rect["y"] < 0:
            ActionChains(self.driver).send_keys_to_element(self.target, Keys.ARROW_UP).perform()

        self.chat_input = self.query_selector('#input_area')
        self.chat_input.send_keys("message")

        self.last_message = self.query_selector(".message_container:last-child")

        time.sleep(1)

        assert self.last_message.rect['y'] <= 660

    @pytest.mark.gpux5
    def test_if_the_inputbox_expands_shrinks_when_the_user_adds_and_removes_content_from_it(self):

        self.chat_input = self.query_selector('#input_area')

        assert self.chat_input.rect["height"] in range(55,61)

        self.chat_input.send_keys("H".join(["A" for _ in range (300)]))

        assert self.chat_input.rect["height"] in range(200,225)

        while self.chat_input.get_attribute('value'): 
            self.chat_input.send_keys(Keys.BACKSPACE)
        
        assert self.chat_input.rect["height"] in range(55,61) #{'height': 102, 'width': 731, 'x': 290, 'y': 652}