"""
SIEG Hub — Portal Central V2.1
Ecosistema de Inteligencia Geopolítica
Fix: cada bloque HTML en su propio st.markdown para evitar
     que Streamlit sanitice el HTML complejo anidado.
"""

import streamlit as st
import datetime
import json
import os
import math

# ─── PAGE CONFIG ─────────────────────────────────────────────────
st.set_page_config(
    page_title="SIEG Intelligence Hub — Geopolitical Early Warning System",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── SEO ─────────────────────────────────────────────────────────
st.markdown("""
<meta name="description" content="SIEG — Sistema de Inteligencia de Eventos Geopolíticos. Monitor OSINT en tiempo real: conflictos, infraestructura crítica, crisis Iran.">
<meta name="keywords" content="geopolitica, inteligencia, OSINT, Iran, conflicto, infraestructura critica, early warning, SIEG">
<meta name="author" content="M. Castillo">
<meta property="og:title" content="SIEG Intelligence Hub">
<meta property="og:description" content="Sistema de detección temprana de escalada cinética. 14 actores · 6 ejes · Monitor Iran.">
<meta name="robots" content="index, follow">
""", unsafe_allow_html=True)

# ─── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&family=Teko:wght@400;500;600&display=swap');

:root {
    --bg:      #060810;
    --bg2:     #0b0e18;
    --bg3:     #101520;
    --accent:  #00e5ff;
    --red:     #ff3333;
    --orange:  #ff8c00;
    --green:   #00ff88;
    --gold:    #ffd700;
    --muted:   #3a4a6a;
    --text:    #c8d8f0;
    --border:  #1a2540;
}

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif;
}
.block-container { max-width: 100% !important; padding: 0 !important; }
section[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent !important; }
.stDeployButton { display: none; }
.stMarkdown p { color: var(--text) !important; }
div[data-testid="column"] { padding: 0 0.6rem !important; }

/* scanlines */
.stApp::before {
    content:'';
    position:fixed; top:0; left:0; right:0; bottom:0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 3px,
        rgba(0,229,255,0.010) 3px, rgba(0,229,255,0.010) 4px
    );
    pointer-events:none; z-index:9999;
}

/* ── HERO ── */
.hub-hero {
    background:
        radial-gradient(ellipse at 15% 60%, rgba(0,229,255,0.07) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 20%, rgba(255,51,51,0.05) 0%, transparent 50%),
        linear-gradient(180deg, #080a1c 0%, #060810 100%);
    border-bottom: 1px solid var(--border);
    padding: 3rem 4rem 2.5rem;
    position: relative; overflow: hidden;
    margin-bottom: 0;
}
.hub-hero::after {
    content:''; position:absolute; bottom:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent 0%, var(--accent) 30%, var(--accent) 70%, transparent 100%);
    opacity:0.35;
}
.hero-eyebrow {
    font-family:'Share Tech Mono',monospace; font-size:0.72em;
    color:var(--accent); letter-spacing:0.3em; opacity:0.65;
    margin-bottom:0.6rem;
}
.hero-title {
    font-family:'Teko',sans-serif; font-size:5em; font-weight:600;
    line-height:0.92; letter-spacing:0.04em; color:#ffffff;
    text-shadow: 0 0 80px rgba(0,229,255,0.18);
}
.hero-title span { color:var(--accent); }
.hero-sub {
    font-family:'Share Tech Mono',monospace; font-size:0.84em;
    color:#5a7090; margin-top:0.9rem; letter-spacing:0.07em;
}
.hero-badge {
    display:inline-block;
    background:rgba(0,229,255,0.07); border:1px solid rgba(0,229,255,0.22);
    color:var(--accent); font-family:'Share Tech Mono',monospace;
    font-size:0.65em; padding:3px 10px; border-radius:2px;
    letter-spacing:0.15em; margin-right:6px; margin-top:1rem;
}
.hero-live {
    display:inline-block;
    background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.28);
    color:var(--green); font-family:'Share Tech Mono',monospace;
    font-size:0.65em; padding:3px 10px; border-radius:2px;
    letter-spacing:0.15em; margin-top:1rem;
    animation: livepulse 2s ease infinite;
}
.hero-watermark {
    position:absolute; right:3rem; top:50%; transform:translateY(-50%);
    font-family:'Teko',sans-serif; font-size:11em; font-weight:700;
    color:rgba(0,229,255,0.04); line-height:1;
    user-select:none; pointer-events:none; letter-spacing:0.05em;
}

/* ── STATUS BAR ── */
.status-bar {
    background:var(--bg2); border-bottom:1px solid var(--border);
    padding:0.65rem 4rem;
    font-family:'Share Tech Mono',monospace; font-size:0.70em;
    color:var(--muted); display:flex; align-items:center;
    gap:2rem; flex-wrap:wrap;
}
.sdot-g { display:inline-block; width:6px; height:6px; border-radius:50%;
          background:var(--green); box-shadow:0 0 5px var(--green);
          margin-right:5px; animation:blink 2s ease infinite; }
.sval { color:var(--text); font-weight:bold; }

/* ── MODULE CARD ── */
.mod-card {
    background:var(--bg2); border:1px solid var(--border);
    border-radius:4px; position:relative; overflow:hidden;
    transition:transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height:100%;
}
.mod-card:hover { transform:translateY(-4px); }
.mod-card-top { height:3px; width:100%; }
.mod-card-body { padding:1.6rem 1.8rem 1.8rem; }

.mod-tag {
    font-family:'Share Tech Mono',monospace; font-size:0.60em;
    letter-spacing:0.22em; text-transform:uppercase;
    opacity:0.55; margin-bottom:0.7rem;
}
.mod-title {
    font-family:'Teko',sans-serif; font-size:2.5em; font-weight:500;
    letter-spacing:0.04em; line-height:1; color:#fff; margin-bottom:0.4rem;
}
.mod-desc {
    font-family:'Rajdhani',sans-serif; font-size:0.90em;
    color:#4a5e78; line-height:1.55; margin-bottom:1.3rem; min-height:2.8rem;
}

/* ── GAUGE (SVG circular) ── */
.gauge-row {
    display:flex; align-items:center; gap:1rem;
    background:rgba(0,0,0,0.28); border:1px solid var(--border);
    border-radius:3px; padding:0.9rem 1rem; margin-bottom:1.1rem;
}
.gsvg { position:relative; width:86px; height:86px; flex-shrink:0; }
.gsvg svg { width:86px; height:86px; transform:rotate(-90deg); }
.gcenter {
    position:absolute; inset:0;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    font-family:'Teko',sans-serif;
}
.gnum  { font-size:1.55em; font-weight:600; line-height:1; }
.gpct  { font-size:0.52em; opacity:0.55; letter-spacing:0.1em; }

.ginfo { flex:1; }
.glabel { font-family:'Share Tech Mono',monospace; font-size:0.60em; color:var(--muted); letter-spacing:0.12em; text-transform:uppercase; }
.glevel { font-family:'Rajdhani',sans-serif; font-size:1.05em; font-weight:600; margin-top:3px; }
.gactors { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); margin-top:5px; }

/* ── MINI BARS ── */
.mbars { margin-bottom:1.3rem; }
.mrow  { display:flex; align-items:center; gap:7px; margin-bottom:5px; }
.mlbl  { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); width:72px; flex-shrink:0; }
.mtrack { flex:1; height:3px; background:rgba(255,255,255,0.05); border-radius:2px; overflow:hidden; }
.mfill  { height:100%; border-radius:2px; }
.mval   { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); width:26px; text-align:right; flex-shrink:0; }

/* ── CTA ── */
.cta {
    display:block; text-align:center; text-decoration:none !important;
    padding:0.65rem 1rem; border-radius:2px;
    font-family:'Share Tech Mono',monospace; font-size:0.70em;
    letter-spacing:0.14em; text-transform:uppercase; font-weight:bold;
    transition:filter 0.2s ease;
}
.cta:hover { filter:brightness(1.4); }
.cta::after { content:' →'; }
.cta-g { background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.35); color:var(--green) !important; }
.cta-b { background:rgba(0,229,255,0.07); border:1px solid rgba(0,229,255,0.35); color:var(--accent) !important; }
.cta-r { background:rgba(255,51,51,0.07);  border:1px solid rgba(255,51,51,0.35);  color:var(--red) !important; }

/* ── GLOBAL PANEL ── */
.gpanel {
    background:var(--bg2); border:1px solid var(--border);
    border-radius:4px; padding:2rem 2.5rem; margin:1.5rem 0 0;
}
.gpanel-title {
    font-family:'Teko',sans-serif; font-size:1.4em; color:var(--gold);
    letter-spacing:0.12em; text-transform:uppercase;
    border-bottom:1px solid var(--border); padding-bottom:0.7rem; margin-bottom:1.3rem;
}
.kpi-grid {
    display:grid; grid-template-columns:repeat(4,1fr);
    gap:1px; background:var(--border);
    border:1px solid var(--border); border-radius:3px; overflow:hidden;
    margin-bottom:1.5rem;
}
.kpi-cell {
    background:var(--bg3); padding:1.1rem; text-align:center;
}
.kpi-lbl { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); letter-spacing:0.12em; margin-bottom:0.4rem; }
.kpi-val { font-family:'Teko',sans-serif; font-size:2.6em; font-weight:600; line-height:1; }
.kpi-sub { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); margin-top:3px; }

.info-grid { display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; }
.info-head { font-family:'Share Tech Mono',monospace; font-size:0.62em; color:var(--muted); letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.7rem; }
.info-body { font-family:'Rajdhani',sans-serif; font-size:0.88em; color:#3a5070; line-height:1.75; }
.info-mono { font-family:'Share Tech Mono',monospace; font-size:0.66em; color:#2a4060; line-height:2.0; }
.info-mono span { color:var(--accent); }

/* ── FOOTER ── */
.hub-footer {
    background:var(--bg2); border-top:1px solid var(--border);
    padding:1.8rem 4rem; margin-top:2rem;
    display:flex; justify-content:space-between; align-items:center;
    font-family:'Share Tech Mono',monospace; font-size:0.66em;
    color:var(--muted); flex-wrap:wrap; gap:1rem;
}
.hub-footer a { color:var(--accent); text-decoration:none; }

/* ── ANIMATIONS ── */
@keyframes blink    { 0%,100%{opacity:1} 50%{opacity:0.15} }
@keyframes livepulse{ 0%,100%{opacity:1} 50%{opacity:0.6}  }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ─────────────────────────────────────────────────────

def load_score(path: str, default: float = 45.0) -> float:
    try:
        with open(path) as f:
            return float(json.load(f).get("score", default))
    except Exception:
        return default

def load_crisis(path: str, default: float = 65.0) -> float:
    try:
        with open(path) as f:
            return float(json.load(f).get("crisis_score", default))
    except Exception:
        return default

def score_level(s):
    if s >= 80: return "CRÍTICO", "#ff3333"
    if s >= 60: return "ALTO",    "#ff8c00"
    if s >= 40: return "MEDIO",   "#ffd700"
    return             "NORMAL",  "#00ff88"

def build_gauge(score: int, color: str) -> str:
    r    = 33
    circ = 2 * math.pi * r
    fill = round(circ * score / 100, 1)
    gap  = round(circ - fill, 1)
    return (
        f'<div class="gsvg">'
        f'<svg viewBox="0 0 86 86">'
        f'<circle cx="43" cy="43" r="{r}" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="6"/>'
        f'<circle cx="43" cy="43" r="{r}" fill="none" stroke="{color}" stroke-width="6"'
        f' stroke-dasharray="{fill} {gap}" stroke-linecap="round"'
        f' style="filter:drop-shadow(0 0 5px {color})"/>'
        f'</svg>'
        f'<div class="gcenter">'
        f'<span class="gnum" style="color:{color}">{score}</span>'
        f'<span class="gpct">%</span>'
        f'</div>'
        f'</div>'
    )

def build_bars(items: dict, color: str) -> str:
    html = '<div class="mbars">'
    for label, val in items.items():
        v = int(val)
        html += (
            f'<div class="mrow">'
            f'<span class="mlbl">{label}</span>'
            f'<div class="mtrack"><div class="mfill" style="width:{v}%;background:{color};'
            f'box-shadow:0 0 4px {color}55;"></div></div>'
            f'<span class="mval">{v}%</span>'
            f'</div>'
        )
    html += '</div>'
    return html

def build_card(
    card_class, top_gradient,
    tag_color, tag_text,
    title, desc,
    score, items,
    gauge_label, gauge_actors,
    cta_class, cta_url, cta_text
) -> str:
    level, color = score_level(score)
    gauge        = build_gauge(score, color)
    bars         = build_bars(items, color)

    return f"""
<div class="mod-card {card_class}" style="border-top:3px solid {top_gradient[0]};">
  <div class="mod-card-top" style="background:linear-gradient(90deg,{top_gradient[0]},{top_gradient[1]});height:3px;"></div>
  <div class="mod-card-body">
    <div class="mod-tag" style="color:{tag_color};">▸ {tag_text}</div>
    <div class="mod-title">{title}</div>
    <div class="mod-desc">{desc}</div>
    <div class="gauge-row">
      {gauge}
      <div class="ginfo">
        <div class="glabel">{gauge_label}</div>
        <div class="glevel" style="color:{color};">{level}</div>
        <div class="gactors">{gauge_actors}</div>
      </div>
    </div>
    {bars}
    <a class="cta {cta_class}" href="{cta_url}" target="_blank">{cta_text}</a>
  </div>
</div>
"""


# ─── DATOS LIVE ───────────────────────────────────────────────────

BASE = os.path.dirname(os.path.abspath(__file__))
C    = os.path.join(BASE, "..", "SIEG-Core",  "data")
A    = os.path.join(BASE, "..", "SIEG-Atlas", "data", "live")
I    = os.path.join(BASE, "..", "SIEG-Iran",  "data", "live")

core_actors = {
    "Iran/M.Or":  load_score(os.path.join(C, "geoint_iran_m_oriente.json"), 68),
    "Rusia/Ucr":  load_score(os.path.join(C, "geoint_rusia_ucrania.json"),  62),
    "China":      load_score(os.path.join(C, "geoint_china.json"),          38),
    "N.Korea":    load_score(os.path.join(C, "geoint_north_korea.json"),    35),
}
atlas_modules = {
    "Maritimo":  load_score(os.path.join(A, "atlas_maritimo.json"),  45),
    "Petroleo":  load_score(os.path.join(A, "atlas_petroleo.json"),  35),
    "MarChina":  load_score(os.path.join(A, "atlas_marchina.json"),  42),
    "Ciber":     load_score(os.path.join(A, "atlas_ciber.json"),     33),
}
iran_vectors = {
    "Conflicto": load_score(os.path.join(I, "iran_conflicto_directo.json"),  72),
    "Nuclear":   load_score(os.path.join(I, "iran_nuclear.json"),            68),
    "Proxies":   load_score(os.path.join(I, "iran_proxies_regionales.json"), 70),
    "Hormuz":    load_score(os.path.join(I, "iran_energia_hormuz.json"),     65),
}

core_score  = int(sum(core_actors.values())  / len(core_actors))
atlas_score = int(sum(atlas_modules.values()) / len(atlas_modules))
iran_score  = int(load_crisis(os.path.join(I, "iran_crisis_summary.json"), 65))
global_score = int(core_score * 0.45 + iran_score * 0.35 + atlas_score * 0.20)

gl_level, gl_color = score_level(global_score)

n_alert = (sum(1 for v in core_actors.values()  if v >= 60) +
           sum(1 for v in atlas_modules.values() if v >= 50) +
           sum(1 for v in iran_vectors.values()  if v >= 60))

now     = datetime.datetime.now()
now_str = now.strftime("%d %b %Y · %H:%M UTC")


# ─── HERO ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hub-hero">
  <div class="hero-watermark">SIEG</div>
  <div style="max-width:860px;position:relative;z-index:1;">
    <div class="hero-eyebrow">▸ Sistema de Inteligencia de Eventos Geopolíticos · OSINT Early Warning</div>
    <div class="hero-title">SIEG<span>.</span>HUB</div>
    <div class="hero-sub">Open Source Intelligence &nbsp;·&nbsp; 14 Actores · 6 Ejes · Monitor Iran · Nodo Odroid-C2</div>
    <div style="margin-top:1rem;">
      <span class="hero-badge">OSINT</span>
      <span class="hero-badge">GEOPOLÍTICA</span>
      <span class="hero-badge">INFRAESTRUCTURA</span>
      <span class="hero-badge">IRAN CRISIS</span>
      <span class="hero-live">&#x25CF; EN VIVO</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── STATUS BAR ──────────────────────────────────────────────────
st.markdown(f"""
<div class="status-bar">
  <span><span class="sdot-g"></span>Todos los sistemas operativos</span>
  <span>🕐 <span class="sval">{now_str}</span></span>
  <span>AMENAZA GLOBAL: <span class="sval" style="color:{gl_color};">{gl_level} · {global_score}%</span></span>
  <span>VECTORES EN ALERTA: <span class="sval" style="color:#ff8c00;">{n_alert}</span></span>
  <span style="margin-left:auto;opacity:0.35;">{now.strftime('%Y-%m-%d')}</span>
</div>
""", unsafe_allow_html=True)

# ─── CARDS — 3 columnas Streamlit ────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(build_card(
        card_class    = "card-core",
        top_gradient  = ("#00ff88", "#00aa55"),
        tag_color     = "#00ff88",
        tag_text      = "Módulo 01 · Geopolítica Global",
        title         = "SIEG CORE",
        desc          = "Motor principal. 14 actores geopolíticos, 3 capas OSINT, autolearning y detección de disonancia narrativa.",
        score         = core_score,
        items         = core_actors,
        gauge_label   = "Índice de tensión",
        gauge_actors  = "14 actores · Ciclo 60 min",
        cta_class     = "cta-g",
        cta_url       = "https://sieg-intelligence-radar.streamlit.app/",
        cta_text      = "Acceder a SIEG Core",
    ), unsafe_allow_html=True)

with col2:
    st.markdown(build_card(
        card_class    = "card-atlas",
        top_gradient  = ("#00e5ff", "#0077aa"),
        tag_color     = "#00e5ff",
        tag_text      = "Módulo 02 · Infraestructura Crítica",
        title         = "SIEG ATLAS",
        desc          = "6 ejes de infraestructura crítica: energía, rutas marítimas, cables submarinos, espacio y ciberespacio.",
        score         = atlas_score,
        items         = atlas_modules,
        gauge_label   = "Índice de riesgo",
        gauge_actors  = "6 ejes · Ciclo 60 min",
        cta_class     = "cta-b",
        cta_url       = "https://sieg-atlas-intelligence.streamlit.app/",
        cta_text      = "Acceder a SIEG Atlas",
    ), unsafe_allow_html=True)

with col3:
    st.markdown(build_card(
        card_class    = "card-iran",
        top_gradient  = ("#ff3333", "#aa2200"),
        tag_color     = "#ff3333",
        tag_text      = "Módulo 03 · Sala de Crisis",
        title         = "SIEG IRAN",
        desc          = "Monitor Iran-Israel. 8 vectores: nuclear, proxies, Hormuz, teatro regional y posición de potencias.",
        score         = iran_score,
        items         = iran_vectors,
        gauge_label   = "Índice de crisis",
        gauge_actors  = "8 vectores · Ciclo 60 min",
        cta_class     = "cta-r",
        cta_url       = "https://sieg-iran-crisis.streamlit.app/",
        cta_text      = "Acceder a SIEG Iran",
    ), unsafe_allow_html=True)

# ─── GLOBAL THREAT PANEL ─────────────────────────────────────────
st.markdown(f"""
<div class="gpanel">
  <div class="gpanel-title">◈ Matriz de Amenaza Global</div>
  <div class="kpi-grid">
    <div class="kpi-cell">
      <div class="kpi-lbl">ÍNDICE GLOBAL</div>
      <div class="kpi-val" style="color:{gl_color};text-shadow:0 0 20px {gl_color}40;">{global_score}%</div>
      <div class="kpi-sub" style="color:{gl_color};">{gl_level}</div>
    </div>
    <div class="kpi-cell">
      <div class="kpi-lbl">VECTORES TOTALES</div>
      <div class="kpi-val" style="color:#ff8c00;">28</div>
      <div class="kpi-sub">14 + 6 + 8 monitorizados</div>
    </div>
    <div class="kpi-cell">
      <div class="kpi-lbl">EN ALERTA</div>
      <div class="kpi-val" style="color:#ff3333;">{n_alert}</div>
      <div class="kpi-sub">score ≥ 60%</div>
    </div>
    <div class="kpi-cell">
      <div class="kpi-lbl">FUENTES OSINT</div>
      <div class="kpi-val" style="color:#00e5ff;">120+</div>
      <div class="kpi-sub">RSS · autolearning 3 capas</div>
    </div>
  </div>
  <div class="info-grid">
    <div>
      <div class="info-head">Metodología OSINT</div>
      <div class="info-body">
        Análisis léxico multi-fuente ponderado por CF (Coeficiente de Fiabilidad) ·
        Autolearning 3 capas: primarias → fallback → Google News ·
        Detección de disonancia narrativa · Suelos dinámicos por actor ·
        Flash News: extracción automática de eventos críticos (TTL 48h)
      </div>
    </div>
    <div>
      <div class="info-head">Infraestructura</div>
      <div class="info-mono">
        <span>■</span> Nodo físico: Odroid-C2 ARM · DietPi v9.x<br>
        <span>■</span> Ciclo scan: 60 min · Git sync automático<br>
        <span>■</span> Scanners: Core V9.3 · Atlas V1.3 · Iran V1.1<br>
        <span>■</span> Dashboards: Streamlit Cloud · Acceso público libre
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="hub-footer">
  <div>
    🛡 <strong style="color:var(--text);">SIEG Intelligence Hub</strong> &nbsp;·&nbsp;
    © {now.year} <strong>M. Castillo</strong> &nbsp;·&nbsp;
    <a href="mailto:mybloggingnotes@gmail.com">mybloggingnotes@gmail.com</a>
  </div>
  <div style="text-align:right;">
    Datos de fuentes abiertas (OSINT) &nbsp;·&nbsp; Solo uso informativo &nbsp;·&nbsp;
    {now_str}
  </div>
</div>
""", unsafe_allow_html=True)
