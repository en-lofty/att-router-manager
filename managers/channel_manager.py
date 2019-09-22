from __future__ import annotations

from typing import Union

from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from driver_singleton import DriverSingleton
from utilities import requires_url


class ChannelManager:
    _ADVANCED_SETTINGS_URL = "http://192.168.1.254/xslt?PAGE=C_2_1c"
    _channel_select_element: WebElement
    _driver = DriverSingleton.get_driver()

    @classmethod
    @requires_url(required_url=_ADVANCED_SETTINGS_URL)
    def get_options(cls):
        cls._get_channel_element()
        return [option.text for option in Select(cls.channel_select_element).options]

    @classmethod
    def _get_channel_element(cls, _2_4ghz=True):
        if _2_4ghz:
            cls._channel_select_element = cls._driver.find_element_by_id("CHANNEL")
        else:
            cls._channel_select_element = cls._driver.find_element_by_id("CHANNEL_WIFI0")

    @classmethod
    def _set_channel(cls, value: Union[str, int]):
        select = Select(cls.channel_select_element)
        if str(value) in [op.text for op in select.options]:
            select.select_by_value(str(value))
            logger.info(f"Set channel to {value}")
        else:
            logger.error(f"No such channel: {value}")
            DriverSingleton.close()

    @classmethod
    @requires_url(required_url=_ADVANCED_SETTINGS_URL)
    def set_channel(cls, value: Union[str, int]):
        cls._get_channel_element()
        cls._set_channel(value)
        cls._save()

    @classmethod
    @requires_url(required_url=_ADVANCED_SETTINGS_URL)
    def get_channel(cls):
        cls._get_channel_element()
        select = Select(cls._channel_select_element)
        return select.first_selected_option.text

    @classmethod
    def _save(cls):
        logger.info("Saving settings...")
        cls._driver.find_element(By.NAME, "SAVE").click()
        logger.info("Channel changes saved.")
