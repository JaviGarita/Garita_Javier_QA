"""Módulo de validaciones y reglas de negocio para ShopGo."""


def validar_password(password: str) -> bool:
    """Valida si una contraseña cumple con las reglas de ShopGo.

    Reglas:
    - Debe ser una cadena de texto (str).
    - Longitud entre 8 y 20 caracteres (inclusive).
    - Al menos una letra mayúscula.
    - Al menos un número (dígito).
    - Ningún espacio en blanco.
    """
    if not isinstance(password, str):
        return False

    if not (8 <= len(password) <= 20):
        return False

    if any(caracter.isspace() for caracter in password):
        return False

    tiene_mayuscula = any(caracter.isupper() for caracter in password)
    tiene_numero = any(caracter.isdigit() for caracter in password)

    return tiene_mayuscula and tiene_numero


def calcular_envio(subtotal: float) -> int:
    """Calcula el costo de envío según el subtotal del carrito en ShopGo.

    Reglas:
    - Si el subtotal es negativo (< 0), lanza ValueError.
    - Si el subtotal es de ₡25 000 o más (>= 25000), devuelve 0 (envío gratis).
    - Si el subtotal es menor a ₡25 000 (0 <= subtotal < 25000), devuelve 2500.
    """
    if subtotal < 0:
        raise ValueError("El subtotal no puede ser negativo.")

    if subtotal >= 25000:
        return 0

    return 2500
