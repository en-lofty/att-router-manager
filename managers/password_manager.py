from __future__ import annotations

from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from driver_singleton import DriverSingleton
from utilities import requires_url


class PasswordManager:
    _ADVANCED_SETTINGS_URL = "http://192.168.1.254/xslt?PAGE=C_2_1c"
    _driver = DriverSingleton.get_driver()  # type: WebDriver

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def set_password(cls, new_password: str, _2_4gz: bool):
        """
        Enables or disables the broadcasting
        """
        element_id = 'USER_KEY' if _2_4gz else 'USER_KEY_WIFI'
        element = cls._driver.find_element_by_id(element_id)
        logger.info(f'Setting {"2.4gz" if _2_4gz else "5ghz"}\'s password successfully changed.')
        element.clear()
        element.send_keys(new_password)
        input()
        cls._save()

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def get_password(cls, _2_4gz: bool) -> bool:
        element_id = 'USER_KEY' if _2_4gz else 'USER_KEY_WIFI'
        element = cls._driver.find_element_by_id(element_id)
        return element.get_attribute('value')

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def _save(cls):
        logger.info("Saving settings...")
        cls._driver.find_element(By.NAME, "SAVE").click()
        logger.info("Channel changes saved.")
