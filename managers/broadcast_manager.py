from __future__ import annotations

from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from driver_singleton import DriverSingleton
from utilities import requires_url


class BroadcastManager:
    _ADVANCED_SETTINGS_URL = "http://192.168.1.254/xslt?PAGE=C_2_1c"
    _driver = DriverSingleton.get_driver()  # type: WebDriver

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def set_broadcast(cls, enabled: bool, _2_4gz: bool):
        """
        Enables or disables the broadcasting
        """
        element_id = 'ESSID_BCAST_WL0_USER' if _2_4gz else 'ESSID_BCAST_WIFI0_USER'
        element = cls._driver.find_element_by_id(element_id)
        select = Select(element)
        logger.info(f'Setting {"2.4gz" if _2_4gz else "5ghz"} broadcast to {enabled}')
        select.select_by_value("1" if enabled else "0")
        cls._save()

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def is_broadcasting(cls, _2_4gz: bool) -> bool:
        element_id = 'ESSID_BCAST_WL0_USER' if _2_4gz else 'ESSID_BCAST_WIFI0_USER'
        element = cls._driver.find_element_by_id(element_id)
        select = Select(element)
        return True if select.first_selected_option.text == "Enabled" else False

    @classmethod
    @requires_url(_ADVANCED_SETTINGS_URL)
    def _save(cls):
        logger.info("Saving settings...")
        cls._driver.find_element(By.NAME, "SAVE").click()
        logger.info("Channel changes saved.")
