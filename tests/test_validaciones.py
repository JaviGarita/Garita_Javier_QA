"""Pruebas unitarias para las funciones de validación y cálculo de envío de ShopGo."""

import pytest
from shopgo.validaciones import calcular_envio, validar_password


# =====================================================================
# Pruebas para validar_password
# =====================================================================

@pytest.mark.parametrize(
    "password, resultado_esperado",
    [
        ("Abcdef1", False),                 # 7 caracteres (límite inferior - 1)
        ("Abcdef12", True),                 # 8 caracteres (límite inferior exacto)
        ("Abcdefghijklmnopqr12", True),     # 20 caracteres (límite superior exacto)
        ("Abcdefghijklmnopqrs12", False),   # 21 caracteres (límite superior + 1)
    ],
    ids=[
        "7_caracteres_invalido",
        "8_caracteres_valido",
        "20_caracteres_valido",
        "21_caracteres_invalido",
    ],
)
def test_validar_password_valores_limite_longitud(password, resultado_esperado):
    """Verifica los valores límite de longitud de la contraseña (7, 8, 20 y 21 caracteres)."""
    assert validar_password(password) is resultado_esperado


@pytest.mark.parametrize(
    "password_valida",
    [
        "ShopGo123",          # Caso estándar con mayúscula, minúsculas y números
        "ABCDEFG1",           # Solo mayúsculas y un número (sin minúsculas)
        "ShopGo123!@#",       # Con caracteres especiales permitidos
    ],
    ids=[
        "estandar_alfanumerica",
        "solo_mayusculas_y_numero",
        "con_caracteres_especiales",
    ],
)
def test_validar_password_casos_positivos_validos(password_valida):
    """Verifica que contraseñas válidas que cumplen todas las reglas devuelvan True."""
    assert validar_password(password_valida) is True


@pytest.mark.parametrize(
    "password_invalida",
    [
        "shopgo1234",         # Mayúscula faltante
        "ShopGoApp",          # Número faltante
        "ShopGo 123",         # Espacio en blanco intermedio
        " ShopGo123",         # Espacio en blanco al inicio
        "ShopGo123 ",         # Espacio en blanco al final
        "ShopGo\t123",        # Carácter de tabulación
        "        ",           # Solo espacios (8 caracteres)
        "",                   # Texto vacío
        None,                 # Valor None
    ],
    ids=[
        "sin_mayuscula",
        "sin_numero",
        "con_espacio_intermedio",
        "con_espacio_inicial",
        "con_espacio_final",
        "con_tabulacion",
        "solo_espacios",
        "texto_vacio",
        "valor_none",
    ],
)
def test_validar_password_casos_negativos(password_invalida):
    """Verifica que contraseñas sin mayúscula, sin número, con espacios, vacías o None devuelvan False."""
    assert validar_password(password_invalida) is False


# =====================================================================
# Pruebas para calcular_envio
# =====================================================================

@pytest.mark.parametrize(
    "subtotal, envio_esperado",
    [
        (0, 2500),            # Límite inferior no negativo (0)
        (1, 2500),            # Mínimo entero positivo
        (24999, 2500),        # Límite justo debajo de envío gratis (entero)
        (24999.99, 2500),     # Límite justo debajo de envío gratis (decimal)
        (25000, 0),           # Límite exacto para envío gratis
        (25000.01, 0),        # Límite justo arriba de envío gratis (decimal)
        (25001, 0),           # Límite justo arriba de envío gratis (entero)
        (100000, 0),          # Monto alto con envío gratis
    ],
    ids=[
        "subtotal_0_cobra_envio",
        "subtotal_1_cobra_envio",
        "subtotal_24999_cobra_envio",
        "subtotal_24999_99_cobra_envio",
        "subtotal_25000_envio_gratis",
        "subtotal_25000_01_envio_gratis",
        "subtotal_25001_envio_gratis",
        "subtotal_100000_envio_gratis",
    ],
)
def test_calcular_envio_valores_limite_y_particiones(subtotal, envio_esperado):
    """Verifica el cálculo de envío en valores límite (0, 24999, 25000, 25001) y particiones equivalentes."""
    assert calcular_envio(subtotal) == envio_esperado


@pytest.mark.parametrize(
    "subtotal_negativo",
    [
        -0.01,                # Límite negativo decimal inmediato a cero
        -1,                   # Límite negativo entero inmediato a cero
        -25000,               # Monto negativo alto
    ],
    ids=[
        "subtotal_menos_0_01",
        "subtotal_menos_1",
        "subtotal_menos_25000",
    ],
)
def test_calcular_envio_subtotal_negativo_lanza_value_error(subtotal_negativo):
    """Verifica que un subtotal negativo lance una excepción ValueError."""
    with pytest.raises(ValueError):
        calcular_envio(subtotal_negativo)
