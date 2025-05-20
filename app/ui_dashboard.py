import streamlit as st
import matplotlib.pyplot as plt

def mostrar_panel_metricas():
    st.subheader("📌 Panel de Métricas y Gráficos")

    col_m1, _ = st.columns(2)
    with col_m1:
        if st.button("🧹 Limpiar métricas"):
            st.session_state.metricas_personalizadas = []

    metricas = st.session_state.metricas_personalizadas

    if metricas:
        # Mostrar en filas de 2 columnas
        for i in range(0, len(metricas), 2):
            col1, col2 = st.columns(2)

            for j, col in enumerate([col1, col2]):
                if i + j >= len(metricas):
                    break
                elemento = metricas[i + j]
                tipo = elemento["tipo"]

                with col:
                    if tipo == "metrica":
                        st.metric(label=elemento["titulo"], value=elemento["valor"])

                    elif tipo == "grafico":
                        st.markdown(f"**{elemento['titulo']}**")
                        df = elemento["data"]

                        tipo_grafico = st.selectbox(
                            "Tipo de gráfico",
                            ["Barras", "Líneas", "Pastel"],
                            index=["Barras", "Líneas", "Pastel"].index(elemento["chart"]),
                            key=f"grafico_{i+j}"
                        )
                        elemento["chart"] = tipo_grafico

                        if tipo_grafico == "Barras":
                            st.bar_chart(df.set_index(df.columns[0]))
                        elif tipo_grafico == "Líneas":
                            st.line_chart(df.set_index(df.columns[0]))
                        elif tipo_grafico == "Pastel":
                            fig, ax = plt.subplots()
                            ax.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct="%1.1f%%")
                            ax.axis("equal")
                            st.pyplot(fig)
    else:
        st.info("🔍 Aún no has generado métricas ni gráficos. Usa el asistente para comenzar.")