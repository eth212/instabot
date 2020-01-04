import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

user_name_global = raw_input()
p_word_global = raw_input()
hashtag_global = raw_input()


chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
chrome_options.add_argument("--disable-infobars")

class Insta:
    def __init__(self, username, password, hashtag):
        self.password = password
        self.username = username
        self.hashtag = hashtag
        self.bot = webdriver.Chrome(chrome_options=chrome_options)

    def login(self):
        bot = self.bot
        bot.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(3)
        email = bot.find_element_by_name("username")
        password = bot.find_element_by_name("password")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(1)
        #asks about notifications
        notifs = bot.find_element_by_class_name("HoLwm")
        notifs.send_keys(Keys.RETURN)

    def like_post(self):
        bot = self.bot
        bot.get("https://www.instagram.com/explore/tags/" + self.hashtag)
        time.sleep(3)
        for i in range(3):
            bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
        post_class = bot.find_elements_by_class_name("v1Nh3")
        for i in range(50):
            bot.get(post_class[i].find_element_by_tag_name("a").get_attribute("href"))
            time.sleep(1)
            bot.find_element_by_class_name("fr66n").find_element_by_tag_name("button").click()


account = Insta(user_name_global, p_word_global, hashtag_global)
account.login()
account.like_post()
