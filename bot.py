# Copyright 2020 Ethan Bonnardeaux
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random

''' instagram limits :
Source # 1
    Followers:
        Account active for months:
        follow/unfollow ~= 20 users per hour and 100-200 users per day
        Account active for Years:
        follow/unfollow ~= 50 users per hour and 300-400 users per day

    Likes:
        350 likes per hour

Source # 2
    Trusted accounts
        Likes: 1 every 28 – 36 seconds, or 1000 at a time using scheduling tools -> 24-hour break after hitting the limit
        Follows: 1 every 28 – 38 seconds, under 200 an hour. 1000 follows a day and below 200 an hour (1000 a day, with a 24-hour break);
        Comments: under 12-14 an hour, with a 350 – 400-second break between each one
        DMs: 50 to 100 DMs/day.
    New accounts
        For the first 12 to 20 days, you need to wait 36-48 seconds between any actions.
        Daily limit is 500 actions a day (follow, unfollow, like).
        New accounts can expect to send anywhere from 20-50 DMs/day

'''


chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
chrome_options.add_argument("--disable-infobars")

class Insta:
    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.bot = webdriver.Chrome(chrome_options=chrome_options)

    def login(self):
        bot = self.bot
        bot.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        email =  WebDriverWait(bot, 10).until( EC.presence_of_element_located((By.NAME, "username")))
        password = bot.find_element_by_name("password")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        notifs = WebDriverWait(bot, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "HoLwm")))
        notifs.send_keys(Keys.RETURN)

    def like_post(self, hashtag):
        bot = self.bot
        bot.get("https://www.instagram.com/explore/tags/" + hashtag)
        WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "o64aR")))

        for i in range(10):      #gets 216 episodes
            bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1.5)

        post_class = bot.find_elements_by_class_name("v1Nh3")

        links = []
        for i in range(10):     #getting all the links
            links.append(post_class[i].find_element_by_tag_name("a").get_attribute("href"))

        for j in range(10):
            time.sleep(1)
            bot.get(links[j])
            time.sleep(1)
            bot.find_element_by_class_name("fr66n").find_element_by_tag_name("button").click()

    def comment_post(self, list_of_comments, hashtag):
        #note : could analyze photos using CNN's to create comments based on the photos
        bot = self.bot
        bot.get("https://www.instagram.com/explore/tags/" + hashtag)
        WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "o64aR")))

        for i in range(10):      #gets 216 episodes
            bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1.5)

        post_class = bot.find_elements_by_class_name("v1Nh3")

        links = []
        for i in range(9,19):     #getting all the links
            links.append(post_class[i].find_element_by_tag_name("a").get_attribute("href"))

        for j in range(10):
            time.sleep(1)
            bot.get(links[j])
            time.sleep(1)

            #open the comment box
            comment_div = bot.find_element_by_class_name("RxpZH")
            comment_div.click()

            comment_box = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Ypffh")))
            user_comment = random.randint(0,len(list_of_comments) - 1)

            print(list_of_comments[user_comment])
            comment_box.send_keys(list_of_comments[user_comment])

            comment_div.find_element_by_tag_name("button").click()

    def comment_and_like(self, list_of_comments, hashtag):
        bot = self.bot
        bot.get("https://www.instagram.com/explore/tags/" + hashtag)
        WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "o64aR")))

        for i in range(10):      #gets 216 episodes
            bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1.5)

        post_class = bot.find_elements_by_class_name("v1Nh3")

        links = []
        for i in range(9,19):     #getting all the links
            links.append(post_class[i].find_element_by_tag_name("a").get_attribute("href"))

        for j in range(10):
            time.sleep(1)
            bot.get(links[j])
            time.sleep(1)
            bot.find_element_by_class_name("fr66n").find_element_by_tag_name("button").click()
            time.sleep(1)
            #open the comment box
            comment_div = bot.find_element_by_class_name("RxpZH")
            comment_div.click()

            comment_box = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Ypffh")))
            user_comment = random.randint(0,len(list_of_comments) - 1)

            print(list_of_comments[user_comment])
            comment_box.send_keys(list_of_comments[user_comment])

            comment_div.find_element_by_tag_name("button").click()


account = Insta("user name", "password")
account.login()
account.like_post()
account.comment_post(["cool", "nice", "nice shot"], "hashtag")
