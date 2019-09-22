import os
import sys
from typing import Union

from logzero import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver


class LoginListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        super().before_navigate_to(url, driver)
        logger.info(f"Navigating to {url}")

    def after_navigate_to(self, url: str, driver: WebDriver):
        super().after_navigate_to(url, driver)
        try:
            driver.find_element_by_id("ADM_PASSWORD")
            logger.info("Auto-login activated")
            DriverSingleton.login()
            logger.info("Logged in")
        except NoSuchElementException:
            pass


class DriverSingleton:
    SETTINGS_URL = "http://192.168.1.254/xslt?PAGE=C_2_1"
    ACCESS_CODE = "47%35146#9"
    __instance: 'DriverSingleton' = None

    def __init__(self, headless: bool):
        if DriverSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            options = Options()
            options.headless = headless
            driver = webdriver.Firefox(options=options,
                                       executable_path=os.path.join(sys.path[0],
                                                                    "./bin/geckodriver"),
                                       log_path=os.path.join(sys.path[0],
                                                             "./logs/geckodriver.log"))
            driver.implicitly_wait(10)
            # driver.set_page_load_timeout(10)
            self.driver = EventFiringWebDriver(driver, LoginListener())
            DriverSingleton.__instance = self

    @staticmethod
    def get_driver():
        return DriverSingleton.__instance.driver

    @staticmethod
    def get_instance():
        if DriverSingleton.__instance is None:
            DriverSingleton(True)
        return DriverSingleton.__instance

    @staticmethod
    def login():
        # fill in password
        pass_input = DriverSingleton.__instance.driver.find_element_by_id("ADM_PASSWORD")
        pass_input.send_keys(DriverSingleton.ACCESS_CODE)
        pass_input.send_keys(Keys.RETURN)

    @staticmethod
    def close(reason: Union[str, int] = 0):
        try:
            DriverSingleton.__instance.driver.close()
        except AttributeError:
            pass
        finally:
            exit(reason)
