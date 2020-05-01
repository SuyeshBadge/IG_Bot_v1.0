from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import sys


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

        time.sleep(0.52)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(0.52)

    def like_photo(self, hashtag):
        driver = self.driver
        notnow = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')))
        notnow.click()
        # if You Want To Change The Link You Can Change it Here
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")

        time.sleep(0.52)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 12):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.52)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(0.5)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(1)
                like_button = lambda: driver.find_element_by_css_selector(
                    '#react-root > section > main > div > div.ltEKP > article > div.eo2As > section.ltpMr.Slqrh > '
                    'span.fr66n > button > svg').click()
                like_button().click()
                time.sleep(1)
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(1)
            except Exception as e:
                time.sleep(0.52)

                # Following The page
            try:
                time.sleep(1)
                follow_button = lambda: driver.find_element_by_css_selector(
                    '#react-root > section > main > div > div.ltEKP > article > header > div.o-MQd.z8cbW > '
                    'div.PQo_0.RqtMr > div.bY2yH > button').click()
                follow_button().click()
                time.sleep(1)
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(1)
            except Exception as e:
                time.sleep(0.52)

            unique_photos -= 1


if __name__ == "__main__":

    username = ""  # Enter Username Here
    password = ""  # Enter Password Here

    ig = InstagramBot(username, password)
    ig.login()

    hashtags = ['tiktokindia']

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            ig.like_photo(tag)
        except Exception:
            ig.closeBrowser()
            time.sleep(6)
            ig = InstagramBot(username, password)
            ig.login()
