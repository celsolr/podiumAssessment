import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import HtmlTestRunner
from os.path import dirname, join
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..."))
from Pages.mainPage import MainPage

project_root = dirname(dirname(__file__))
results_path = join(project_root, 'Results')

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chrome_options = Options()
        cls.chrome_options.add_argument("--headless")
        cls.chrome_options.add_argument("--no-sandbox")
        cls.chrome_options.add_argument("--disable-dev-shm-usage")
        cls.chrome_options.add_argument("--disable-extensions")
        cls.chrome_options.add_argument("--disable-gpu")
        cls.chrome_options.add_argument("disable-infobars")

        cls.driver = webdriver.Chrome(options=cls.chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()


    # verifies that bubble message is displayed upon page load and can be closed
    def test_01_bubble_message_display(self):
        driver = self.driver
        main = MainPage(driver)

        main.load()
        self.assertTrue(main.bubble_message_displayed())
        main.close_bubble_message()
        self.assertFalse(main.bubble_message_displayed())

    # verifies that contact modal can be opened/closed with button and closed clicking outside the modal
    def test_02_contact_modal_display(self):
        driver = self.driver
        main = MainPage(driver)

        main.load()
        main.open_close_contact_modal()
        self.assertTrue(main.contact_modal_displayed())

        main.open_close_contact_modal()
        self.assertFalse(main.contact_modal_displayed())

        main.open_close_contact_modal()
        self.assertTrue(main.contact_modal_displayed())

        main.click_outside_modal()
        self.assertFalse(main.contact_modal_displayed())

    # verifies that a message cannot be sent with empty fields
    def test_03_message_empty_fields(self):
        driver = self.driver
        main = MainPage(driver)

        main.load()
        main.open_close_contact_modal()
        main.click_submit_button()
        self.assertFalse(main.message_sent())

    # verifies that videos can be played and closed
    def test_04_verify_play_close_video(self):
        driver = self.driver
        main = MainPage(driver)

        main.load()
        main.play_video()
        main.close_video()

    # validates all links in the page and saves results in csv file (Results folder)
    def test_05_verify_links(self):
        driver = self.driver
        main = MainPage(driver)

        main.load()
        self.assertTrue(main.get_links() == 0)


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=results_path))
