import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from core.prompt_builder import build_prompt
from core.gemini_client import get_sql_query
from core.sql_executor import fetch_sql
from utils.validator_query import is_valid_sql, clean_sql
from config import DB_CONFIG

def mostrar_chat_asistente():
    st.subheader("💬 Asistente NL2SQL (Proyecto de tesis)")

    with st.expander("ℹ️ Ayuda contextual: ¿Qué puedo consultar?"):
        st.markdown("### 🗃️ Tablas disponibles")
        st.markdown("""
        - **clientes**: `id`, `nombre`, `email`, `fecha_registro`  
        - **productos**: `id`, `nombre`, `precio`, `categoria_id`  
        - **categorias**: `id`, `nombre`  
        - **ordenes**: `id`, `cliente_id`, `producto_id`, `cantidad`, `fecha_orden`, `sucursal_id`  
        - **pagos**: `id`, `orden_id`, `monto`, `metodo`, `fecha_pago`  
        - **envios**: `id`, `orden_id`, `fecha_envio`, `estado`, `direccion`  
        - **empleados**: `id`, `nombre`, `cargo`, `sucursal_id`, `fecha_contratacion`  
        - **sucursales**: `id`, `nombre`, `ciudad`  
        """)

        st.markdown("### ❓ Ejemplos de preguntas útiles")
        st.markdown("""
        - ¿Cuántos clientes hay registrados por ciudad?  
        - ¿Cuál es el total de ingresos por método de pago?  
        - ¿Cuántos productos hay por categoría?  
        - ¿Qué pedidos están pendientes de entrega?  
        - ¿Cuál fue el ingreso total por sucursal en 2024?  
        - ¿Quién es el empleado más antiguo?  
        """)

        st.markdown("### 💡 Recomendaciones")
        st.markdown("""
        - Redacta tus preguntas con claridad  
        - El sistema es solo de lectura (no modifica datos)  
        - Puedes exportar los resultados o graficarlos si aplican  
        """)
    col_c1, _ = st.columns(2)
    with col_c1:
        if st.button("🧹 Limpiar chat"):
            st.session_state.chat = []

    with st.container():
        for autor, mensaje in st.session_state.chat:
            with st.chat_message(autor):
                st.markdown(mensaje)

    sugerencias = [
        "¿Cuál es el total de ventas este mes?",
        "¿Cuántos productos se han vendido?",
        "¿Cuál es el ingreso total por producto?",
        "¿Cuántos clientes hay?",
        "¿Cuánto se ganó este año?"
    ]
    placeholder = f"Ej: {sugerencias[len(st.session_state.chat) % len(sugerencias)]}"
    pregunta = st.chat_input(placeholder=placeholder)

    if pregunta:
        st.session_state.chat.append(("user", pregunta))

        schema = open("app/schemas/database_schema.txt").read()
        prompt = build_prompt(schema, pregunta)
        sql_raw = get_sql_query(prompt)
        sql_clean = clean_sql(sql_raw)
        st.session_state.sql = sql_clean

        st.session_state.chat.append(("assistant", f"**Consulta SQL generada:**\n```sql\n{sql_clean}\n```"))
        print(f"Consulta SQL generada:\n{sql_clean}\n")

        if is_valid_sql(sql_clean):
            try:
                resultado = fetch_sql(DB_CONFIG, sql_clean)
                st.session_state.resultado = resultado

                if resultado.shape == (1, 1) and pd.api.types.is_numeric_dtype(resultado.iloc[0, 0]):
                    nombre = pregunta.capitalize().rstrip("?")
                    valor = resultado.iloc[0, 0]
                    if not any(m["titulo"] == nombre and m["tipo"] == "metrica" for m in st.session_state.metricas_personalizadas):
                        st.session_state.metricas_personalizadas.append({
                            "tipo": "metrica",
                            "titulo": nombre,
                            "valor": valor
                        })
                        st.session_state.chat.append((
                            "assistant",
                            f"**Resultado (métrica):** {valor}"
                        ))
                        st.rerun()

                elif resultado.shape[1] == 2 and pd.api.types.is_numeric_dtype(resultado.iloc[:, 1]):
                    nombre = pregunta.capitalize().rstrip("?")
                    st.session_state.metricas_personalizadas.append({
                        "tipo": "grafico",
                        "titulo": nombre,
                        "data": resultado,
                        "chart": "Barras"
                    })
                    st.session_state.chat.append((
                        "assistant",
                        f"**Resultado (gráfico):**\n{resultado.to_markdown(index=False)}"
                    ))
                    st.rerun()
                    
                else:
                    # ✅ Mostrar resultados generales
                    nombre = pregunta.capitalize().rstrip("?")

                    st.success("✅ Resultado obtenido:")

                                    # Añadir explícitamente al chat
                    st.session_state.chat.append((
                        "assistant",
                        f"**Resultado:**\n\n{resultado.to_markdown(index=False)}"
                    ))
                    print('estamos aca')
                    st.rerun()


            except Exception as e:
                st.session_state.resultado = None
                st.session_state.chat.append(("assistant", f"❌ Error: {e}"))
                st.error(f"❌ Error al ejecutar consulta: {e}")
        else:
            st.session_state.chat.append(("assistant", "⚠️ Consulta no válida."))
            st.session_state.resultado = None
            st.error("❌ Consulta SQL no válida. Por favor, revisa la consulta generada.")
