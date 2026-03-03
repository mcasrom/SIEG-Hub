import streamlit as st
import datetime

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL (favicon, título, layout)
# ---------------------------------------------------------
st.set_page_config(
    page_title="SIEG Dashboard",
    page_icon="assets/sieg_icon.png",
    layout="wide"
)

# ---------------------------------------------------------
# ESTILOS GLOBALES (tema premium SIEG)
# ---------------------------------------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1E293B;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transition: 0.2s ease-in-out;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}
.card h3 {
    margin-top: 0;
}

.button {
    background-color: #00AEEF;
    color: white !important;
    padding: 10px 18px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
}
.button:hover {
    background-color: #0095D1;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER CON LOGO
# ---------------------------------------------------------
col_logo, col_title = st.columns([1,4])

with col_logo:
    st.image("assets/sieg_logo.png", width=140)

with col_title:
    st.markdown("<h1 style='margin-top: 25px;'>SIEG Dashboard</h1>", unsafe_allow_html=True)
    st.write("Portal central del ecosistema de inteligencia geopolítica SIEG.")

st.divider()

# ---------------------------------------------------------
# TARJETAS PREMIUM
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🛰️ SIEG-Core</h3>
        <p>Motor principal de análisis geopolítico.</p>
        <a class="button" href="https://sieg-intelligence-radar.streamlit.app/" target="_blank">Entrar</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🌍 SIEG-Atlas</h3>
        <p>Mapa estratégico global.</p>
        <a class="button" href="https://sieg-atlas-intelligence.streamlit.app/" target="_blank">Entrar</a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🇮🇷 SIEG-Iran</h3>
        <p>Monitor especializado en Irán.</p>
        <a class="button" href="https://sieg-iran-crisis.streamlit.app/" target="_blank">Entrar</a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# RESUMEN GLOBAL
# ---------------------------------------------------------
st.subheader("📊 Resumen Global")
st.write("""
Este panel ofrece una visión general del ecosistema SIEG.  
Para análisis detallados, accede a cada módulo desde las tarjetas superiores.
""")

# ---------------------------------------------------------
# FOOTER PROFESIONAL
# ---------------------------------------------------------
st.markdown("""
<hr style="margin-top: 50px; margin-bottom: 10px; border: 1px solid #334155;">
""", unsafe_allow_html=True)

timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

footer_html = f"""
<div style='text-align: center; color: #94A3B8; font-size: 14px; margin-top: 20px;'>
    <p>© {datetime.datetime.now().year} M. Castillo — 
    <a href="mailto:mybloggingnotes@gmail.com" style="color:#00AEEF;">mybloggingnotes@gmail.com</a></p>
    <p>Última actualización: {timestamp}</p>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
