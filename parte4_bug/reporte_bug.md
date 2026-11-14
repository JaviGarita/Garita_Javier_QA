# Parte 4 — Reporte de Bug

## Título
**[Carrito] La cantidad de unidades de un producto se reinicia a 1 al rotar la pantalla del dispositivo**

---

## Entorno
- **Dispositivo:** Samsung (modelo específico no detallado en el reporte original).
- **Sistema Operativo:** Android 13.
- **Versión de la app (ShopGo):** No especificada por el usuario *(ver sección de Preguntas Abiertas)*.

---

## Precondiciones
- Tener la aplicación **ShopGo** instalada y una sesión de usuario activa.
- Tener habilitada la función de **rotación automática de pantalla** en el dispositivo móvil.
- Contar con disponibilidad del producto ("camisa") en el catálogo.

## Pasos para reproducirlo
1. Abrir la aplicación **ShopGo** con el dispositivo en orientación vertical (*portrait*).
2. Agregar el producto "camisa" al carrito de compras.
3. Ir a la pantalla del **Carrito de compras** y establecer la cantidad del producto en **3 unidades** (verificando que el indicador muestre `3`).
4. Girar físicamente el teléfono para cambiar la orientación de la pantalla a horizontal (*landscape*).
5. Observar el valor mostrado en el selector de cantidad del producto dentro del carrito.

---

## Resultado esperado y resultado actual
- **Resultado esperado:** Al rotar la pantalla, el carrito de compras conserva el estado actual y mantiene la cantidad de **3 camisas** (así como el subtotal correspondiente).
- **Resultado actual:** Al rotar el teléfono, la cantidad de camisas en el carrito se pierde y se restablece a **1 unidad**.

---

## Severidad y Prioridad
- **Severidad: Media** — Provoca pérdida del estado de datos en el carrito al recrearse la vista por cambio de orientación, alterando las unidades seleccionadas y potencialmente el subtotal y cálculo de envío (ej. perder el envío gratis de ₡25 000), aunque no produce un cierre inesperado (*crash*) y permite reajustar la cantidad manualmente.
- **Prioridad: Media** — Impacta directamente la experiencia de compra y la exactitud del pedido en dispositivos Android con rotación activa, por lo que debe corregirse antes del siguiente lanzamiento sin llegar a bloquear el uso general de la aplicación.

---

## Evidencia que adjuntaría
1. **Grabación de pantalla (Video / Screen Recording):** Mostrando el flujo completo desde que se seleccionan las 3 unidades en el carrito, el momento exacto de la rotación del dispositivo y cómo el valor vuelve a `1`.
2. **Capturas de pantalla (Screenshots):** Una captura en orientación vertical con la cantidad en `3` y otra inmediatamente después de girar a horizontal mostrando la cantidad en `1` (para evidenciar también si el subtotal y el costo de envío cambiaron).
3. **Logs del dispositivo (`adb logcat`) y tráfico de red:** Registro de eventos durante la rotación para verificar cómo se maneja el ciclo de vida de la `Activity`/`Fragment` (`onSaveInstanceState` / `ViewModel`) y confirmar si el reinicio ocurre solo en el estado local de la UI o si dispara una petición al servidor.

---

## Preguntas Abiertas (Información Faltante)
Dado que el reporte original del usuario es breve, se plantean las siguientes preguntas abiertas para acotar la causa raíz:
1. **¿En qué versión exacta de la app ShopGo ocurre el problema?** (ej. `v1.2.0` producción o build de pruebas).
2. **¿Cuál es el modelo exacto del teléfono Samsung y versión de One UI?** (ej. Galaxy S23, Galaxy A54, o un dispositivo plegable como Galaxy Z Fold).
3. **¿El fallo ocurre únicamente con el producto "camisas" o se reproduce con cualquier producto del catálogo?**
4. **¿Sucede con cualquier cantidad distinta de 1 dentro del rango permitido (de 2 a 10 unidades)?** ¿Siempre vuelve a `1` sin importar la cantidad previa?
5. **¿El problema ocurre al rotar de vertical a horizontal, de horizontal a vertical, o en ambos sentidos?**
6. **¿Al cambiar la cantidad a 1 también se recalcula el subtotal del carrito (y se guarda en backend), o es únicamente un reinicio visual del componente selector en pantalla?**
