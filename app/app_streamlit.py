from ui_dashboard import mostrar_panel_metricas
from ui_chat import mostrar_chat_asistente
import streamlit as st

st.set_page_config(page_title="NL2SQL Dashboard", layout="wide")

for key, default in {
    "chat": [],
    "metricas_personalizadas": [],
    "resultado": None,
    "sql": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("📊 NL2SQL Dashboard + Asistente")
col1, col2 = st.columns([2, 3])

with col1:
    mostrar_panel_metricas()

with col2:
    mostrar_chat_asistente()
