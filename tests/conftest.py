"""Configuración de fixtures de pytest para las pruebas de ShopGo."""

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def driver():
    """Inicializa el driver de Appium con capabilities de ejemplo para ShopGo y lo cierra al finalizar."""
    capabilities = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "emulator-5554",
        "appium:platformVersion": "13.0",
        "appium:appPackage": "com.shopgo.app",
        "appium:appActivity": "com.shopgo.app.MainActivity",
        "appium:noReset": False,
    }

    options = UiAutomator2Options().load_capabilities(capabilities)
    appium_server_url = "http://127.0.0.1:4723"

    app_driver = webdriver.Remote(command_executor=appium_server_url, options=options)
    yield app_driver
    app_driver.quit()
