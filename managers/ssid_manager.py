from __future__ import annotations

from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from driver_singleton import DriverSingleton
from utilities import requires_url


class SSIDManager:
    _ADVANCED_SETTINGS_URL = "http://192.168.1.254/xslt?PAGE=C_2_1c"
    _driver = DriverSingleton.get_driver()  # type: WebDriver

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def set_ssid(cls, new_name: str, _2_4gz: bool):
        """
        Enables or disables the broadcasting
        """
        element_id = 'ESSID_WL0_USER' if _2_4gz else 'ESSID_WIFI0_USER'
        element = cls._driver.find_element_by_id(element_id)
        logger.info(f'Setting {"2.4gz" if _2_4gz else "5ghz"}\'s SSID to {new_name}')
        element.clear()
        element.send_keys(new_name)
        logger.info(f'{"2.4gz" if _2_4gz else "5ghz"}\'s SSID has been set to {new_name}')

        cls._save()

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def get_ssid(cls, _2_4gz: bool) -> bool:
        element_id = 'ESSID_WL0_USER' if _2_4gz else 'ESSID_WIFI0_USER'
        element = cls._driver.find_element_by_id(element_id)
        return element.get_attribute('value')

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def _save(cls):
        logger.info("Saving settings...")
        cls._driver.find_element(By.NAME, "SAVE").click()
        logger.info("Channel changes saved.")
