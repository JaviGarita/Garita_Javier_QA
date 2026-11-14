"""Pruebas automatizadas de UI mobile para la pantalla de inicio de sesión de ShopGo."""

from pages.login_page import LoginPage


def test_inicio_sesion_exitoso_muestra_titulo_bienvenido(driver):
    """Verifica que al iniciar sesión con credenciales válidas se muestre el título 'Bienvenido'."""
    login_page = LoginPage(driver)

    login_page.iniciar_sesion("usuario@dominio.com", "ShopGo123")

    assert login_page.obtener_titulo_principal() == "Bienvenido"


def test_inicio_sesion_fallido_muestra_mensaje_error(driver):
    """Verifica que al iniciar sesión con datos incorrectos se muestre el mensaje de error esperado."""
    login_page = LoginPage(driver)

    login_page.iniciar_sesion("usuario@dominio.com", "ClaveIncorrecta1")

    assert login_page.obtener_mensaje_error() == "Correo o contraseña incorrectos"
