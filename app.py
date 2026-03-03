import streamlit as st

st.set_page_config(page_title="SIEG Intelligence Hub", page_icon="🌐", layout="wide")

st.title("🌐 SIEG Intelligence Hub")
st.write("Portal central del ecosistema de inteligencia geopolítica SIEG.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🛰️ SIEG-Core")
    st.write("Motor principal de análisis geopolítico.")
    st.success("Estado: Online")
    st.link_button("Entrar", "https://sieg-intelligence-radar.streamlit.app/")

with col2:
    st.subheader("🌍 SIEG-Atlas")
    st.write("Mapa estratégico global.")
    st.success("Estado: Online")
    st.link_button("Entrar", "https://sieg-atlas-intelligence.streamlit.app/")

with col3:
    st.subheader("🇮🇷 SIEG-Iran")
    st.write("Monitor especializado en Irán.")
    st.success("Estado: Online")
    st.link_button("Entrar", "https://sieg-iran-crisis.streamlit.app/")

st.divider()

st.subheader("📊 Resumen Global (versión ligera)")
st.write("""
Este panel ofrece una visión general del ecosistema SIEG.  
Para análisis detallados, accede a cada módulo desde las tarjetas superiores.
""")
