"""Page Object para la pantalla de inicio de sesión de ShopGo."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    """Representa la pantalla de inicio de sesión y sus interacciones."""

    # Locators usando AppiumBy.ACCESSIBILITY_ID
    INPUT_EMAIL = (AppiumBy.ACCESSIBILITY_ID, "input_email")
    INPUT_PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "input_password")
    BTN_LOGIN = (AppiumBy.ACCESSIBILITY_ID, "btn_login")
    TXT_ERROR = (AppiumBy.ACCESSIBILITY_ID, "txt_error")
    HOME_TITLE = (AppiumBy.ACCESSIBILITY_ID, "home_title")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def ingresar_correo(self, correo: str) -> None:
        """Espera a que el campo de correo sea visible, lo limpia e ingresa el correo."""
        campo_correo = self.wait.until(EC.visibility_of_element_located(self.INPUT_EMAIL))
        campo_correo.clear()
        campo_correo.send_keys(correo)

    def ingresar_password(self, password: str) -> None:
        """Espera a que el campo de contraseña sea visible, lo limpia e ingresa la contraseña."""
        campo_password = self.wait.until(EC.visibility_of_element_located(self.INPUT_PASSWORD))
        campo_password.clear()
        campo_password.send_keys(password)

    def tocar_iniciar_sesion(self) -> None:
        """Espera a que el botón 'Iniciar sesión' sea clickeable y lo presiona."""
        boton_login = self.wait.until(EC.element_to_be_clickable(self.BTN_LOGIN))
        boton_login.click()

    def iniciar_sesion(self, correo: str, password: str) -> None:
        """Ejecuta el flujo completo de inicio de sesión con las credenciales dadas."""
        self.ingresar_correo(correo)
        self.ingresar_password(password)
        self.tocar_iniciar_sesion()

    def obtener_mensaje_error(self) -> str:
        """Espera a que aparezca el mensaje de error y devuelve su texto."""
        elemento_error = self.wait.until(EC.visibility_of_element_located(self.TXT_ERROR))
        return elemento_error.text

    def obtener_titulo_principal(self) -> str:
        """Espera a que cargue el título de la pantalla principal y devuelve su texto."""
        elemento_titulo = self.wait.until(EC.visibility_of_element_located(self.HOME_TITLE))
        return elemento_titulo.text
