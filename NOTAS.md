# Notas de la Prueba Técnica — ShopGo QA Automation

## 1. Suposiciones ante Reglas Ambiguas

A partir de la revisión de las reglas de negocio de **ShopGo** (secciones *Pantalla de inicio de sesión* y *Carrito de compras*), se identificaron las siguientes ambigüedades en su redacción y se establecieron las suposiciones correspondientes:

1. **Formato de correo electrónico:**
   - **Regla:** *"El correo debe tener un formato válido (ejemplo: nombre@dominio.com)."*
   - **Ambigüedad:** No se especifica si el correo distingue entre mayúsculas y minúsculas (*case-sensitive*) ni qué sucede si el usuario ingresa espacios accidentales al inicio o al final (comportamiento frecuente en teclados móviles).
   - **Suposición:** El correo electrónico es insensible a mayúsculas/minúsculas (`Usuario@Dominio.com` es equivalente a `usuario@dominio.com`) y la aplicación ignora los espacios en blanco al inicio o al final del texto ingresado.

2. **Composición de la contraseña:**
   - **Regla:** *"La contraseña debe tener entre 8 y 20 caracteres, al menos una mayúscula, al menos un número y ningún espacio."*
   - **Ambigüedad:** La regla no indica qué sucede si se incluyen caracteres especiales (ej. `!@#$%&*`), ni aclara si el uso de letras minúsculas es obligatorio.
   - **Suposición:** Los caracteres especiales y las letras minúsculas están permitidos pero no son obligatorios; basta con cumplir el rango de 8 a 20 caracteres, incluir al menos una letra mayúscula, al menos un número y no contener ningún tipo de espacio en blanco.

3. **Mensaje de error ante datos incorrectos vs. formato inválido:**
   - **Regla:** *"Si los datos son incorrectos, aparece el mensaje 'Correo o contraseña incorrectos'."*
   - **Ambigüedad:** No se distingue si por "datos incorrectos" se refiere únicamente a credenciales que no coinciden con una cuenta registrada, o si también aplica cuando los campos están vacíos o incumplen el formato de correo/contraseña.
   - **Suposición:** Se muestra el mensaje *"Correo o contraseña incorrectos"* ante cualquier intento de inicio de sesión con credenciales inválidas o que no cumplan las reglas de validación al presionar *"Iniciar sesión"*.

4. **Comportamiento durante y después del bloqueo de la cuenta:**
   - **Regla:** *"Después de 3 intentos fallidos seguidos, la cuenta se bloquea por 5 minutos."*
   - **Ambigüedad:** La regla no detalla qué mensaje recibe el usuario al bloquearse la cuenta, qué sucede si intenta iniciar sesión con datos correctos mientras está bloqueada, qué pasa con el contador si inicia sesión con éxito antes del tercer fallo, ni cómo se comporta el sistema al finalizar los 5 minutos.
   - **Suposición:**
     - Al tercer intento fallido consecutivo, el sistema notifica que la cuenta ha sido bloqueada temporalmente por 5 minutos.
     - Durante esos 5 minutos no se permite iniciar sesión aunque se ingresen credenciales válidas.
     - Un inicio de sesión exitoso en el primer o segundo intento reinicia el contador de intentos fallidos a cero.
     - Transcurridos los 5 minutos, la cuenta se desbloquea automáticamente y el contador de intentos fallidos se restablece a cero.

5. **Cantidad de unidades en el carrito de compras:**
   - **Regla:** *"Cada producto admite una cantidad de 1 a 10 unidades."*
   - **Ambigüedad:** No se especifica si el límite de 10 unidades es únicamente por cada producto distinto o si existe un límite máximo de productos diferentes en el carrito, ni cómo se elimina un producto si el mínimo admitido es 1.
   - **Suposición:** El límite de 1 a 10 unidades aplica por línea de producto individual dentro del carrito, existiendo una acción independiente para eliminar el producto del carrito.

---

## 2. Declaración de Uso de Herramientas de IA

En cumplimiento con las normas de la prueba técnica, se declara de forma transparente el uso de inteligencia artificial como asistente durante la resolución:

- **1. ¿Qué herramienta usó?**
  - **Antigravity** (asistente de IA en el IDE impulsado por modelos de Google DeepMind).

- **2. ¿En qué parte de la prueba, para qué y qué revisó o cambió usted? (Desglose por sección)**

| Parte de la prueba | ¿Para qué se usó la IA? (generar código/casos, revisar, depurar) | ¿Qué propuso, revisó o cambió el candidato (Javier Garita)? |
| :--- | :--- | :--- |
| **Análisis de Reglas y Suposiciones (`NOTAS.md`)** | Revisar las observaciones de ambigüedad planteadas por el candidato, identificar casos borde adicionales y estructurar la redacción en Markdown. | Propuse inicialmente las ambigüedades de la Regla 3 (caracteres especiales en contraseña) y Regla 5 (qué ocurre tras el bloqueo de 5 minutos). Revisé la primera versión generada por la IA y **solicité corregir y limitar el alcance** para que las suposiciones se centraran únicamente en las reglas de negocio y su redacción, eliminando detalles de implementación de código. |
| **Parte 1 — Diseño de casos de prueba (`parte1_casos/casos_login.md`)** | Revisar críticamente el listado inicial de casos propuesto por el candidato y dar formato a la tabla final de 12 casos bajo el estándar exigido. | Diseñé y propuse la lista inicial de casos y prioridades (campos vacíos, formato de correo/contraseña, login válido, inyección SQL y los 3 escenarios mobile: pérdida de conexión, rotación de pantalla y app en segundo plano). A partir del feedback recibido, **cambié el alcance descartando los 3 casos del carrito de compras** (para mantener el archivo exclusivo para la pantalla de Login) e incorporé los casos de bloqueo tras 3 intentos y valores límite (`7, 8, 20, 21`). |
| **Parte 2 — Pruebas automatizadas (`shopgo/validaciones.py`, `tests/test_validaciones.py`, `README.md`, `requirements.txt`)** | Generar el código base de las funciones `validar_password` y `calcular_envio`, las pruebas parametrizadas con `pytest.mark.parametrize` y `pytest.raises`, y la documentación del `README.md`. | Revisé la lógica de ambas funciones para confirmar que cumplieran las reglas y las suposiciones definidas (manejo seguro de `None`, rechazo de espacios con `isspace()`, retorno de `2500` para subtotal `0` y `ValueError` para negativos), así como la cobertura de todos los valores límite (`7, 8, 20, 21` caracteres y subtotales `24999` y `25000`). |
| **Parte 3 — Script de UI mobile (`pages/login_page.py`, `tests/conftest.py`, `tests/test_login.py`)** | Generar la estructura del patrón Page Object (`LoginPage`), el fixture del driver en `conftest.py` y los dos tests de UI en `test_login.py`. | Revisé que todos los identificadores coincidieran exactamente con la tabla del enunciado (`AppiumBy.ACCESSIBILITY_ID`: `input_email`, `input_password`, `btn_login`, `txt_error`, `home_title`), que se utilizaran esperas explícitas (`WebDriverWait` + `expected_conditions`) sin ningún `time.sleep`, y que las aserciones verificaran los textos exactos (`"Bienvenido"` y `"Correo o contraseña incorrectos"`). |
| **Parte 4 — Reporte de bug (`parte4_bug/reporte_bug.md`)** | Evaluar el borrador del reporte redactado por el candidato y estructurar el documento final en Markdown. | Redacté la propuesta inicial del reporte e identifiqué las preguntas abiertas fundamentales (falta de versión de la app, validar si ocurre con otros productos y probar con cantidades mayores o menores a 3). Tras revisar el análisis, **ajusté la clasificación separando Severidad de Prioridad (ambas en Media)** al considerar el impacto del reinicio de cantidad sobre el subtotal del carrito y la regla de envío gratis (₡25 000). |

---

## 3. Tiempo Invertido
- **Análisis de reglas y documentación de suposiciones (`NOTAS.md`):** ~18 min
- **Parte 1 — Diseño de casos de prueba (`casos_login.md`):** ~15 min
- **Parte 2 — Funciones y pruebas automatizadas con `pytest` (`validaciones.py`, `test_validaciones.py`, `README.md`):** ~12 min
- **Parte 3 — Script de UI mobile con Appium y Page Object (`login_page.py`, `conftest.py`, `test_login.py`):** ~10 min
- **Parte 4 — Reporte de bug (`reporte_bug.md`):** ~15 min
- **Tiempo total aproximado:** ~70 min (15:05 a 16:18)

---

## 4. Registro de Interacciones con IA (Prompts y Respuestas)

A continuación se documenta de forma íntegra y cronológica el historial de prompts enviados por el candidato y las respuestas generadas por el asistente de IA durante el desarrollo de la prueba.

### Interacción #1 — Análisis inicial del enunciado
- **Fecha/Hora:** 2026-11-14 15:05 (UTC-6)
- **Parte relacionada:** General / Análisis global

**Prompt (Usuario):**
> Eres un experto en QA, vas a ayudarme paso a paso en esta prueba técnica. Quiero que analices el enunciado y yo te voy a ir indicando en que necesito tu ayuda. *(Adjunta PDF: Prueba Técnica — Pasantía QA Automation Mobile)*

**Respuesta (Asistente IA):**
> Desglose estructurado de las reglas de negocio de ShopGo (Login y Carrito de compras) y de las 4 partes evaluadas en la prueba técnica:
> 1. **Reglas de Negocio:** Formato de correo válido, contraseña de 8-20 caracteres (≥1 mayúscula, ≥1 número, sin espacios), mensaje de error al fallar, bloqueo por 5 minutos tras 3 intentos fallidos seguidos, pantalla "Bienvenido" al iniciar sesión, límite de 1 a 10 unidades por producto en carrito y envío gratis a partir de ₡25 000 (₡2 500 si es menor; `ValueError` si es negativo).
> 2. **Estructura de la entrega (100 pts):** Parte 1 (Casos de prueba, 30 pts), Parte 2 (Pruebas automatizadas con pytest, 35 pts), Parte 3 (Script UI mobile con Appium y Page Object, 20 pts), Parte 4 (Reporte de bug, 10 pts) y Entrega/Documentación (`README.md`, `NOTAS.md`, `requirements.txt`, 5 pts).

---

### Interacción #2 — Configuración de bitácora de prompts en `NOTAS.md`
- **Fecha/Hora:** 2026-11-14 15:06 (UTC-6)
- **Parte relacionada:** Entrega / `NOTAS.md`

**Prompt (Usuario):**
> Antes de empezar en sí con la prueba, me gustaria que vayas escribiendo al final del archivo NOTAS.md todos los prompt y respuestas que vayamos teniendo para tener un claro registro de eso, usa un formato claro y estandarizado de md.

**Respuesta (Asistente IA):**
> Se estructura el archivo `NOTAS.md` con las secciones solicitadas en la prueba (Suposiciones, Uso de IA, Tiempo invertido) y se añade al final la sección **Registro de Interacciones con IA (Prompts y Respuestas)** bajo un formato estandarizado (número de interacción, fecha/hora, parte relacionada, bloque de prompt y resumen fiel de la respuesta), registrando las interacciones #1 y #2.

---

### Interacción #3 — Discusión técnica sobre ambigüedades en las reglas de negocio
- **Fecha/Hora:** 2026-11-14 15:16 (UTC-6)
- **Parte relacionada:** Análisis de reglas / `NOTAS.md`

**Prompt (Usuario):**
> Perfecto, Primero tengamos una discusión técnica tu y yo, nada va al archivo hasta que te lo indique. Quisiera hacer anotaciones sobre las reglas, considero ambigua la tercera: "La contraseña debe tener entre 8 y 20 caracteres, al menos una mayúscula, al menos un número y ningún espacio." Ya que no especifica explicitamente que sucede en caso de los caracteres especiales.
> Tampoco veo muy clara la regla 5: "Después de 3 intentos fallidos seguidos, la cuenta se bloquea por 5 minutos." ya que no especifica que debe pasar después del bloqueo.
> Esas dos son las observaciones de mi parte, evalua si tiene valor y tambien indica si detectas ambiguedades en las reglas.

**Respuesta (Asistente IA):**
> Se validan ambas observaciones del candidato como altamente relevantes para QA y se amplían con casos derivados:
> 1. **Contraseña:** Confirmar que caracteres especiales y minúsculas son permitidos pero no obligatorios, y definir que cualquier carácter de espacio en blanco invalida la contraseña.
> 2. **Bloqueo tras 3 intentos:** Definir qué ocurre durante el bloqueo (rechazo incluso con credenciales válidas), al lograr un login antes del 3er intento (reinicio del contador) y tras cumplirse los 5 minutos (desbloqueo automático y reinicio del contador a `0`).
> 3. **Ambigüedades adicionales detectadas:** (a) Alcance del mensaje de error ante datos incorrectos vs. formato inválido; (b) Normalización de correo electrónico (*case-insensitivity* y espacios periféricos); (c) Límites de unidades en el carrito y límite inferior en el subtotal de envío.

---

### Interacción #4 — Registro formal de suposiciones en `NOTAS.md`
- **Fecha/Hora:** 2026-11-14 15:23 (UTC-6)
- **Parte relacionada:** Entrega / `NOTAS.md`

**Prompt (Usuario):**
> Perfecto, entonces agrega ambas, las observaciones por mi parte y las tuyas. todas con la redaccion y deficinición adicional que agregaste.

**Respuesta (Asistente IA):**
> Se redactan e incorporan en la sección **1. Suposiciones ante Reglas Ambiguas** de `NOTAS.md` los puntos acordados y se registran las interacciones #3 y #4 en la bitácora del documento.

---

### Interacción #5 — Refinamiento del alcance de las suposiciones únicamente a la redacción de las reglas
- **Fecha/Hora:** 2026-11-14 15:25 (UTC-6)
- **Parte relacionada:** Análisis de reglas / `NOTAS.md`

**Prompt (Usuario):**
> Espera, hay que hacer una corrección limita las observaciones unicamente a las reglas y su redacción en sí.
> *(Cita las reglas de "Pantalla de inicio de sesión" y "Carrito de compras")*

**Respuesta (Asistente IA):**
> Se corrige la sección **1. Suposiciones ante Reglas Ambiguas** de `NOTAS.md` eliminando cualquier referencia a detalles de implementación de código (funciones de Python o locators de Appium) y limitando el análisis estrictamente al texto de las reglas de negocio de *Pantalla de inicio de sesión* y *Carrito de compras* (formato de correo, composición de contraseña, mensaje de datos incorrectos, ciclo de bloqueo de 5 minutos, unidades por producto y costo de envío).

---

### Interacción #6 — Propuesta y evaluación crítica de los 12 casos de prueba (Parte 1)
- **Fecha/Hora:** 2026-11-14 15:41 (UTC-6)
- **Parte relacionada:** Parte 1 — Diseño de casos de prueba (`parte1_casos/casos_login.md`)

**Prompt (Usuario):**
> De acuerdo, vamos con la parte 1. Vamos a diseñar 12 casos de prueba. Los primeros y de más alta prioridad va ser: 
> -Todo lo relacionado a la autenticación del usario y entrada de datos. 
> No acepte entradas de datos vacias, ni en el correo ni en la contraseña. 
> -El inicio de sesión bloquee intentos de SQL inyeccion. 
> -Validar que el correo tenga el formato correcto. 
> -Que la contraseña tenga el formato especificado. 
> -Que inicie de sesión con credenciales válidas.
> -Que el carrito de compras no acepte realizar una compra en caso de estar vacio.
> -Que no permita números negativos.
> -Que cada producto agregado tenga una cantidad dentro del rango de 1 a 10 articulos por carrito.
> Luego en prioridad media sugiero valdiaciones relacionadas a situaciones propias de desarrollo móvil:
> -Perdida de conexión.
> -Rotación de pantalla.
> -Aplicación enviada a segundo plano.
> Por favor evalua, analiza y critica objetivamente los casos de prueba que sugiero y sugiere adicionales que consideres importantes, sobre todo de prioridad baja.

**Respuesta (Asistente IA):**
> Se realiza una evaluación crítica y objetiva de la lista propuesta para la Parte 1:
> 1. **Corrección crítica de alcance (Carrito vs. Login):** El enunciado de la Parte 1 pide explícitamente *"Escriba entre 8 y 12 casos de prueba para la pantalla de inicio de sesión de ShopGo"* (y el archivo se llama `casos_login.md`). Las reglas del carrito existen en las instrucciones globales porque se usan en la Parte 2 (`calcular_envio`) y en la Parte 4 (reporte de bug al rotar el teléfono con 3 camisas). Incluir 3 casos del carrito en `casos_login.md` quitaría espacio del tope máximo de 12 casos para el Login.
> 2. **Omisiones clave del Login que deben entrar:** Falta cubrir explícitamente la **regla de bloqueo tras 3 intentos fallidos por 5 minutos** y los **valores límite** de longitud de contraseña (`7, 8, 20, 21` caracteres), que el enunciado exige evaluar en la Parte 1 (*"Incluya casos positivos, negativos y de valores límite, y al menos 2 casos propios de mobile"*).
> 3. **Evaluación de SQL Injection:** Es un buen caso de seguridad, pero en una matriz limitada a 12 casos donde se evalúan las reglas de negocio dadas, conviene integrarlo o darle prioridad Media/Baja para no desplazar valores límite ni bloqueo de cuenta.
> 4. **Propuesta estructurada de 12 casos (Alta, Media y Baja):** Se presenta una distribución balanceada de 12 casos exclusivos de Login (Positivos, Negativos, Valores Límite y Escenarios Mobile/Prioridad Baja).

---

### Interacción #7 — Redacción de `parte1_casos/casos_login.md`
- **Fecha/Hora:** 2026-11-14 15:45 (UTC-6)
- **Parte relacionada:** Parte 1 — Diseño de casos de prueba (`parte1_casos/casos_login.md`)

**Prompt (Usuario):**
> Excelentes correcciones escribelos en el archivo parte1_casos/casos_login.md, estrictamente bajo el formato solicitado en la prueba:
> `ID | Título | Precondiciones | Pasos | Resultado esperado | Prioridad`

**Respuesta (Asistente IA):**
> Se genera el archivo `parte1_casos/casos_login.md` con una tabla Markdown bajo el formato exacto requerido (`ID`, `Título`, `Precondiciones`, `Pasos`, `Resultado esperado`, `Prioridad`), documentando los 12 casos de prueba (`TC-01` a `TC-12`) distribuidos en prioridades Alta, Media y Baja.

---

### Interacción #8 — Implementación de la Parte 2 (Funciones, pruebas con pytest, `requirements.txt` y `README.md`)
- **Fecha/Hora:** 2026-11-14 15:55 (UTC-6)
- **Parte relacionada:** Parte 2 — Pruebas automatizadas (`shopgo/validaciones.py`, `tests/test_validaciones.py`, `requirements.txt`, `README.md`)

**Prompt (Usuario):**
> Escribe el código correspondiente a la parte 2:
> *(Cita las instrucciones de la Parte 2: implementación de `validar_password` y `calcular_envio` en `shopgo/validaciones.py`, pruebas con `pytest.mark.parametrize`, casos negativos incluyendo `None`, `pytest.raises`, `requirements.txt` y `README.md`)*

**Respuesta (Asistente IA):**
> Se implementan los archivos solicitados en la Parte 2:
> 1. `shopgo/validaciones.py`: Funciones `validar_password(password: str) -> bool` (validación segura ante `None`, longitud 8-20, al menos una mayúscula, al menos un dígito y sin espacios en blanco) y `calcular_envio(subtotal: float) -> int` (`ValueError` si `< 0`, `0` si `>= 25000`, `2500` si `< 25000`).
> 2. `tests/test_validaciones.py`: Suite de pruebas parametrizadas con `@pytest.mark.parametrize` e `ids` descriptivos para valores límite de contraseña (`7, 8, 20, 21` caracteres), casos válidos (incluyendo solo mayúsculas+número y caracteres especiales), casos negativos (sin mayúscula, sin número, espacios al inicio/medio/final/tabulación/solo espacios, texto vacío `""` y `None`), valores límite de envío (`0, 1, 24999, 24999.99, 25000, 25000.01, 25001, 100000`) y prueba de excepción con `pytest.raises(ValueError)` para subtotales negativos (`-0.01, -1, -25000`).
> 3. `requirements.txt` y `README.md`: Dependencias (`pytest`, `Appium-Python-Client`) y guía paso a paso para crear el entorno virtual, instalar paquetes y ejecutar `pytest tests/test_validaciones.py`.

---

### Interacción #9 — Implementación de la Parte 3 (Page Object, fixture de Appium y pruebas de Login UI)
- **Fecha/Hora:** 2026-11-14 16:01 (UTC-6)
- **Parte relacionada:** Parte 3 — Script de UI mobile (`pages/login_page.py`, `tests/conftest.py`, `tests/test_login.py`)

**Prompt (Usuario):**
> perfecto ahora, ayudame a codear la parte 3:
> *(Cita las instrucciones de la Parte 3: `LoginPage` en `pages/login_page.py` con `AppiumBy.ACCESSIBILITY_ID`, pruebas de login exitoso y fallido en `tests/test_login.py`, `WebDriverWait` en lugar de `time.sleep` y fixture del driver en `tests/conftest.py`)*

**Respuesta (Asistente IA):**
> Se implementan los tres archivos de la Parte 3 siguiendo las buenas prácticas de `Appium-Python-Client` y `pytest`:
> 1. `pages/login_page.py`: Clase `LoginPage` que define los 5 locators mediante tuplas `(AppiumBy.ACCESSIBILITY_ID, ...)` (`input_email`, `input_password`, `btn_login`, `txt_error`, `home_title`), instancia `WebDriverWait` y encapsula las acciones (`ingresar_correo`, `ingresar_password`, `tocar_iniciar_sesion`, `iniciar_sesion`, `obtener_mensaje_error`, `obtener_titulo_principal`) usando `expected_conditions` (`visibility_of_element_located`, `element_to_be_clickable`) sin usar `time.sleep`.
> 2. `tests/conftest.py`: Fixture `driver` con `UiAutomator2Options` y capabilities de ejemplo para Android 13 (`com.shopgo.app`), manejando el ciclo de vida con `yield` y `quit()`.
> 3. `tests/test_login.py`: Pruebas `test_inicio_sesion_exitoso_muestra_titulo_bienvenido` (verifica `"Bienvenido"`) y `test_inicio_sesion_fallido_muestra_mensaje_error` (verifica `"Correo o contraseña incorrectos"`).

---

### Interacción #10 — Evaluación crítica de la propuesta de Reporte de Bug (Parte 4)
- **Fecha/Hora:** 2026-11-14 16:16 (UTC-6)
- **Parte relacionada:** Parte 4 — Reporte de bug (`parte4_bug/reporte_bug.md`)

**Prompt (Usuario):**
> ahora vamos con la parte 4.
> Para el reporte: "Tenía 3 camisas en el carrito, giré el teléfono y la cantidad volvió a 1. Me pasa en mi Samsung con Android 13."
> Mi sugerencia para el reporte es:
> - Título: Perdida de datos al rotar el dispositivo móvil (Android 13).
> - Entorno: Teléfono Samsung con Android 13.
> - Precondiciones y pasos para reproducirlo: Estar en el mismo dispositivo, sistema operativo y versión de la aplicación. Agregar 3 camisas al carrito, girar el telefono.
> - Resultado esperado y resultado actual: Se espera se conserven las 3 camisas agregadas al carrito. Actualmente, se resetea a 1 camisa.
> - Severidad y prioridad, con una línea que justifique cada una. Prioridad baja debido a que no compromete las reglas de negocio de forma directa. Es un concepto de UX que puede ser atendido fácilmente.
> - Evidencia que adjuntaría: Video demostrativo de la situación y logs en caso de haber algun registro útil al realizar la acción de girar el teléfono.
> Considero que es importante que se especifique la versión de la aplicación, pero es información que no se teiene en el reporte. Tambien considero importante el verificar si solo sucede con ese producto, o hay más productos que presentan la misma falla. Por ultimo, verificar si al agregar más o menos de 3 elementos sucede el mismo bug.
> Analiza mi propuesta, evalua y da un criterio objetivo, sugiere correcciones si es necesario.

**Respuesta (Asistente IA):**
> Se analiza objetivamente la propuesta del candidato punto por punto, destacando:
> 1. **Aciertos fuertes:** Excelente identificación de las **preguntas abiertas** (versión de la app faltante, si ocurre con otros productos y con otras cantidades entre 2 y 10 unidades).
> 2. **Correcciones clave sugeridas:**
>    - **Título más específico:** Indicar exactamente *qué* dato se pierde y *dónde* (ej. *"La cantidad de un producto en el carrito de compras se reinicia a 1 al rotar la pantalla"*).
>    - **Severidad vs. Prioridad (Separarlas y ajustar el impacto en negocio):** El enunciado pide justificar **ambas por separado** (una línea para Severidad y una línea para Prioridad). Además, en un e-commerce como ShopGo, que el carrito cambie la cantidad de 3 a 1 **sí impacta las reglas de negocio indirectamente** (altera el subtotal de compra y puede hacer que el usuario pierda el envío gratis de ₡25 000 a ₡2 500 o compre menos unidades de las deseadas). Por tanto, una **Severidad Media** y **Prioridad Media** (con *workaround* de no girar la pantalla o reajustar la cantidad) es técnicamente más precisa que "Baja / solo UX".
>    - **Precondiciones y Pasos numerados:** Separar las precondiciones (sesión iniciada, rotación automática activa, producto en carrito) de los pasos numerados paso a paso.
>    - **Preguntas abiertas adicionales:** Modelo exacto de Samsung (One UI) y si el cambio a 1 ocurre solo visualmente en la UI (por recreación de la `Activity` en Android sin guardar el estado) o también se sobrescribe en el backend/subtotal.

---

### Interacción #11 — Redacción final de `parte4_bug/reporte_bug.md` y cierre de `NOTAS.md`
- **Fecha/Hora:** 2026-11-14 16:18 (UTC-6)
- **Parte relacionada:** Parte 4 — Reporte de bug (`parte4_bug/reporte_bug.md`) y Entrega (`NOTAS.md`)

**Prompt (Usuario):**
> Estoy de acuerdo, agregalo al reporte_bug.md.

**Respuesta (Asistente IA):**
> Se redacta el archivo `parte4_bug/reporte_bug.md` con todas las secciones exigidas (Título, Entorno, Precondiciones, Pasos para reproducirlo, Resultado esperado y actual, Severidad y Prioridad justificadas, Evidencia que adjuntaría y Preguntas abiertas) y se completan las secciones **2. Resumen de Uso de Herramientas de IA** y **3. Tiempo Invertido** en `NOTAS.md`.

---

### Interacción #12 — Refinamiento de la declaración de uso de IA en `NOTAS.md`
- **Fecha/Hora:** 2026-11-14 16:22 (UTC-6)
- **Parte relacionada:** Entrega / `NOTAS.md`

**Prompt (Usuario):**
> Asegura de indicar en NOTAS.md correctamente lo solicitado para el uso de herramientas IA:
> Si las usa, regístrelo en NOTAS.md: qué herramienta usó, en qué parte de la prueba, para qué (generar código o casos, revisar, depurar) y qué revisó o cambió usted.

**Respuesta (Asistente IA):**
> Se actualiza la sección **2. Declaración de Uso de Herramientas de IA** en `NOTAS.md` con una tabla detallada que desglosa explícitamente los 4 elementos requeridos por el enunciado para cada parte de la prueba: (1) qué herramienta se usó (`Antigravity`), (2) en qué parte de la prueba se aplicó, (3) para qué propósito específico (revisar, estructurar o generar código/casos) y (4) qué propuso, revisó o cambió directamente el candidato.







