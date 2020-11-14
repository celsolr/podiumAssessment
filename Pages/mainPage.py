from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import csv
from os.path import dirname, join
import time

class MainPage():

    URL = "https://www.podium.com/"

    # header
    header_xpath = (By.XPATH, "//body[@id='theme-white']/nav/div")

    # contact modal elements
    podium_bubble_iframe = (By.XPATH, "//*[@id = 'podium-bubble']") #iframe to access open/close button
    open_close_chat_button = (By.XPATH, "//div[@id='main']/div/div/div/div/button/div")

    podium_modal_iframe = (By.XPATH, "//*[@id = 'podium-modal']") #modal iframe
    compose_message_modal = (By.XPATH, "//*[@id = 'ComposeMessage']")
    name_textbox = (By.XPATH, "//*[@id = 'Name']")
    phone_textbox = (By.ID, "Mobile Phone")
    message_textbox = (By.ID, "Message")
    submit_button = (By.XPATH, "//button[@type='submit']")  #submit button class contains 'incomplete' when disabled and 'valid' when enabled
    area_outside_modal = (By.XPATH, "//*/text()[normalize-space(.)='']/parent::*")
    confirmation_message = (By.XPATH, "//*[@class = 'ConfirmationMessage__Title']")


    podium_prompt_iframe = (By.XPATH, "//*[@id = 'podium-prompt']") #message iframe
    bubble_message_text = (By.XPATH, "//*[@class = 'Prompt__MessageBubble']")
    message_close_button = (By.XPATH, "//*[@class = 'Prompt__CloseButton']")

    #video elements
    play_video_image = (By.XPATH, "//img[@id='video-1-img']")
    close_video = (By.XPATH, "//button[@id='wistia-vvd1bukwgt-1_popover_popover_close_button']/img")

    project_root = dirname(dirname(__file__))
    results_path = join(project_root, 'Results/')


    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)
        #time.sleep(1)
        try:
            myElem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((self.header_xpath)))
        except TimeoutException:
            print ("Timedout!")

        time.sleep(5)

    def get_links(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(self.results_path + 'links_validation_' + timestr + '.csv', mode='w') as result_file:
            fieldnames = ['link_name', 'link_url', 'status_code']
            writer = csv.DictWriter(result_file, fieldnames=fieldnames)
            writer.writeheader()

            linkElements = self.driver.find_elements(By.TAG_NAME, "a")
            broken_links = 0
            for element in linkElements:
                linkUrl = (element.get_attribute("href"))
                if '/wp-content/' in linkUrl:
                    continue
                linkName = (element.get_attribute("text"))
                req = Request(linkUrl, headers={'User-Agent': 'Mozilla/5.0'})
                try:
                    response = urlopen(req)
                except HTTPError as e:
                    status_code = e.code
                except URLError as e:
                    status_code = e.reason
                else:
                    status_code = response.getcode()
                print(linkName, linkUrl, status_code)
                writer.writerow({'link_name': linkName, 'link_url': linkUrl, 'status_code': status_code})
                if status_code >= 400:
                    broken_links = broken_links + 1
        return broken_links


    def bubble_message_displayed(self):
        try:
            iframe = self.driver.find_element(*self.podium_prompt_iframe)
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(*self.bubble_message_text)
        except NoSuchElementException:
            self.driver.switch_to.default_content()
            return False
        self.driver.switch_to.default_content()
        return True

    def close_bubble_message (self):
        iframe = self.driver.find_element(*self.podium_prompt_iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element(*self.message_close_button).click()
        self.driver.switch_to.default_content()

    def open_close_contact_modal (self):
        iframe = self.driver.find_element(*self.podium_bubble_iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element(*self.open_close_chat_button).click()
        self.driver.switch_to.default_content()
        time.sleep(1)

    def contact_modal_displayed(self):
        try:
            iframe = self.driver.find_element(*self.podium_modal_iframe)
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(*self.compose_message_modal)
        except NoSuchElementException:
            self.driver.switch_to.default_content()
            return False
        self.driver.switch_to.default_content()
        return True

    def enter_contact_name(self, name):
        iframe = self.driver.find_element(*self.podium_modal_iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element(*self.name_textbox).clear()
        self.driver.find_element(*self.name_textbox).send_keys(name)
        self.driver.switch_to.default_content()
        #time.sleep(2)

    def enter_contact_phone(self, phone):
        iframe = self.driver.find_element(*self.podium_modal_iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element(*self.phone_textbox).clear()
        self.driver.find_element(*self.phone_textbox).send_keys(phone)
        self.driver.switch_to.default_content()
        #time.sleep(2)

    def enter_contact_message(self, message):
        iframe = self.driver.find_element(*self.podium_modal_iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element(*self.message_textbox).clear()
        self.driver.find_element(*self.message_textbox).send_keys(message)
        self.driver.switch_to.default_content()
        #time.sleep(2)

    def click_submit_button(self):
        iframe = self.driver.find_element(*self.podium_modal_iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element(*self.submit_button).click()
        self.driver.switch_to.default_content()
        time.sleep(1)

    def message_sent(self):
        try:
            iframe = self.driver.find_element(*self.podium_modal_iframe)
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(*self.confirmation_message)
        except:
            self.driver.switch_to.default_content()
            return False
        self.driver.switch_to.default_content()
        return True

    def click_outside_modal(self):
        self.driver.find_element(*self.area_outside_modal).click()
        time.sleep(1)

    def play_video(self):
        self.driver.find_element(*self.play_video_image).click()
        time.sleep(1)

    def close_video(self):
        try:
            self.driver.find_element(*self.close_video).click()
        except:
            return False
        return True
        time.sleep(1)
