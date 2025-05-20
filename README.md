### Desarrollo de tesisi
Como parte central del proyecto, se implementó una interfaz interactiva utilizando **Streamlit**, que permite a los usuarios realizar preguntas en lenguaje natural y visualizar los resultados en tiempo real mediante un **asistente NL2SQL**.

### 🔧 Funcionalidad general

El panel se divide en dos componentes principales:

* **📌 Panel de Métricas y Gráficos**: muestra los indicadores clave extraídos de la base de datos, incluyendo gráficos dinámicos que se pueden personalizar (barras, líneas o pastel).
* **💬 Asistente NL2SQL**: interpreta las preguntas del usuario, genera una consulta SQL utilizando el modelo Gemini 2.5, ejecuta la consulta sobre PostgreSQL y devuelve los resultados.

### ⚙️ Arquitectura y estructura del código

La estructura del proyecto sigue una organización modular basada en carpetas:

```
/
├── app/
│   ├── core/
│   │   ├── gemini_client.py         # Comunicación con Gemini API
│   │   ├── prompt_builder.py        # Generación de prompt con esquema + pregunta
│   │   └── sql_executor.py          # Ejecución de consultas SQL
│   ├── schemas/
│   │   └── database_schema.txt      # Representación del esquema de BD
│   ├── utils/
│   │   ├── app_streamlit.py         # Lógica principal de la app interactiva
│   │   ├── ui_chat.py               # Módulo de UI para el asistente
│   │   └── ui_dashboard.py          # Módulo de UI para el panel de métricas
│   ├── config.py                    # Parámetros de conexión a PostgreSQL
│   └── main.py                      # Punto de entrada para ejecutar la app
```

### 🧠 Flujo de funcionamiento

1. El usuario ingresa una pregunta en lenguaje natural.
2. Se genera un `prompt` incluyendo el esquema de la base de datos y se envía al modelo **Gemini 2.5**.
3. El modelo responde con una consulta SQL que es validada y ejecutada.
4. Los resultados se interpretan y se presentan:

   * Como **métrica**, si es un valor numérico único.
   * Como **gráfico**, si son pares clave-valor.
   * Como **tabla**, si es una consulta general.
5. La consulta y sus resultados quedan registrados en el historial del chat para referencia futura.

### 🧪 Funciones destacadas

* Limpieza del historial de chat y métricas.
* Exportación de resultados a CSV.
* Validación de seguridad en la consulta SQL.
* Soporte para múltiples formatos visuales.
* Interfaz minimalista y responsive.

---

