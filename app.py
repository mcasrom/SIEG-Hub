"""
SIEG Hub — Portal Central V2.0
Ecosistema de Inteligencia Geopolítica
"""

import streamlit as st
import datetime
import time
import json
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────
st.set_page_config(
    page_title="SIEG Intelligence Hub — Geopolitical Early Warning System",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── SEO META INJECTION ──────────────────────────────────────────
st.markdown("""
<head>
<meta name="description" content="SIEG — Sistema de Inteligencia de Eventos Geopolíticos. Monitor OSINT en tiempo real: conflictos, infraestructura crítica, crisis de Iran. Powered by open sources.">
<meta name="keywords" content="geopolitica, inteligencia, OSINT, Iran, conflicto, infraestructura critica, monitor, early warning, SIEG">
<meta name="author" content="M. Castillo">
<meta property="og:title" content="SIEG Intelligence Hub">
<meta property="og:description" content="Sistema de detección temprana de escalada cinética. 14 actores · 6 ejes · Monitor Iran.">
<meta property="og:type" content="website">
<meta name="robots" content="index, follow">
</head>
""", unsafe_allow_html=True)

# ─── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&family=Teko:wght@400;500;600&display=swap');

:root {
    --bg:       #060810;
    --bg2:      #0b0e18;
    --bg3:      #101520;
    --accent:   #00e5ff;
    --red:      #ff3333;
    --orange:   #ff8c00;
    --green:    #00ff88;
    --gold:     #ffd700;
    --muted:    #3a4a6a;
    --text:     #c8d8f0;
    --border:   #1a2540;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif;
}

.block-container {
    max-width: 100% !important;
    padding: 0 !important;
}

/* ── SCANLINES OVERLAY ── */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 3px,
        rgba(0, 229, 255, 0.012) 3px,
        rgba(0, 229, 255, 0.012) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── HEADER HERO ── */
.hub-hero {
    background:
        radial-gradient(ellipse at 20% 50%, rgba(0,229,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(255,51,51,0.05) 0%, transparent 50%),
        linear-gradient(180deg, #08091a 0%, #060810 100%);
    border-bottom: 1px solid var(--border);
    padding: 3rem 4rem 2.5rem;
    position: relative;
    overflow: hidden;
}

.hub-hero::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%, var(--accent) 30%, var(--accent) 70%, transparent 100%);
    opacity: 0.4;
}

.hero-eyebrow {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72em;
    color: var(--accent);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 0.6rem;
    animation: fadeInDown 0.8s ease both;
}

.hero-title {
    font-family: 'Teko', sans-serif;
    font-size: 4.8em;
    font-weight: 600;
    line-height: 0.95;
    letter-spacing: 0.04em;
    color: #ffffff;
    text-shadow: 0 0 60px rgba(0,229,255,0.2);
    animation: fadeInDown 0.9s ease both;
}

.hero-title span {
    color: var(--accent);
}

.hero-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85em;
    color: #6a7fa8;
    margin-top: 1rem;
    letter-spacing: 0.08em;
    animation: fadeInDown 1.0s ease both;
}

.hero-badge {
    display: inline-block;
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.25);
    color: var(--accent);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68em;
    padding: 3px 10px;
    border-radius: 2px;
    letter-spacing: 0.15em;
    margin-right: 8px;
    animation: pulse-border 3s ease infinite;
}

.hero-live {
    display: inline-block;
    background: rgba(0,255,136,0.08);
    border: 1px solid rgba(0,255,136,0.3);
    color: var(--green);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68em;
    padding: 3px 10px;
    border-radius: 2px;
    letter-spacing: 0.15em;
}

.hero-live::before {
    content: '● ';
    animation: blink 1.2s step-end infinite;
}

/* ── STATUS BAR ── */
.status-bar {
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    padding: 0.7rem 4rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72em;
    color: var(--muted);
    flex-wrap: wrap;
}

.status-item { display: flex; align-items: center; gap: 6px; }
.status-dot-green { width: 6px; height: 6px; border-radius: 50%; background: var(--green); box-shadow: 0 0 6px var(--green); animation: blink 2s ease infinite; }
.status-dot-amber { width: 6px; height: 6px; border-radius: 50%; background: var(--orange); box-shadow: 0 0 6px var(--orange); }
.status-val { color: var(--text); font-weight: bold; }

/* ── MAIN GRID ── */
.main-grid {
    padding: 3rem 4rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.8rem;
}

/* ── MODULE CARDS ── */
.module-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 4px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
}

.module-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
}

.card-core::before   { background: linear-gradient(90deg, var(--green), #00aa55); }
.card-atlas::before  { background: linear-gradient(90deg, var(--accent), #0077aa); }
.card-iran::before   { background: linear-gradient(90deg, var(--red), #aa2200); }

.module-card:hover {
    border-color: var(--accent);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,229,255,0.08);
}
.card-iran:hover   { border-color: var(--red); box-shadow: 0 12px 40px rgba(255,51,51,0.1); }
.card-atlas:hover  { border-color: var(--accent); }

.card-inner { padding: 1.8rem 2rem; }

.card-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62em;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    opacity: 0.5;
}
.tag-core  { color: var(--green); }
.tag-atlas { color: var(--accent); }
.tag-iran  { color: var(--red); }

.card-title {
    font-family: 'Teko', sans-serif;
    font-size: 2.4em;
    font-weight: 500;
    letter-spacing: 0.04em;
    line-height: 1;
    margin-bottom: 0.5rem;
    color: #ffffff;
}

.card-desc {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.92em;
    color: #5a6a88;
    line-height: 1.5;
    margin-bottom: 1.5rem;
    min-height: 3rem;
}

/* ── GAUGE CONTAINER ── */
.gauge-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
    padding: 1rem 1.2rem;
    background: rgba(0,0,0,0.3);
    border-radius: 3px;
    border: 1px solid var(--border);
}

.gauge-svg-wrap { position: relative; width: 90px; height: 90px; flex-shrink: 0; }
.gauge-svg-wrap svg { width: 90px; height: 90px; transform: rotate(-90deg); }
.gauge-center {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-family: 'Teko', sans-serif;
}
.gauge-num { font-size: 1.5em; font-weight: 600; line-height: 1; }
.gauge-pct { font-size: 0.55em; opacity: 0.6; letter-spacing: 0.1em; }

.gauge-info { flex: 1; margin-left: 1rem; }
.gauge-label { font-family: 'Share Tech Mono', monospace; font-size: 0.65em; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase; }
.gauge-level { font-family: 'Rajdhani', sans-serif; font-size: 1.1em; font-weight: 600; margin-top: 4px; }
.gauge-actors { font-family: 'Share Tech Mono', monospace; font-size: 0.62em; color: var(--muted); margin-top: 6px; }

/* ── MINI BARS ── */
.mini-bars { margin-bottom: 1.4rem; }
.mini-bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
.mini-bar-label { font-family: 'Share Tech Mono', monospace; font-size: 0.6em; color: var(--muted); width: 80px; flex-shrink: 0; letter-spacing: 0.05em; }
.mini-bar-track { flex: 1; height: 3px; background: rgba(255,255,255,0.05); border-radius: 2px; overflow: hidden; }
.mini-bar-fill { height: 100%; border-radius: 2px; }
.mini-bar-val { font-family: 'Share Tech Mono', monospace; font-size: 0.6em; color: var(--muted); width: 28px; text-align: right; flex-shrink: 0; }

/* ── CTA BUTTON ── */
.cta-btn {
    display: block;
    text-align: center;
    padding: 0.7rem 1.2rem;
    border-radius: 2px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75em;
    letter-spacing: 0.15em;
    text-decoration: none !important;
    font-weight: bold;
    text-transform: uppercase;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}
.btn-core  { background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.4); color: var(--green) !important; }
.btn-atlas { background: rgba(0,229,255,0.08); border: 1px solid rgba(0,229,255,0.4); color: var(--accent) !important; }
.btn-iran  { background: rgba(255,51,51,0.08); border: 1px solid rgba(255,51,51,0.4); color: var(--red) !important; }

.cta-btn:hover { filter: brightness(1.3); transform: none; }
.cta-btn::after { content: ' →'; }

/* ── GLOBAL PANEL ── */
.global-panel {
    margin: 0 4rem 3rem;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2rem 2.5rem;
}

.panel-title {
    font-family: 'Teko', sans-serif;
    font-size: 1.5em;
    color: var(--gold);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.8rem;
}

.threat-matrix {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

.matrix-cell {
    background: var(--bg);
    padding: 1rem;
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
}

.matrix-cell-header {
    background: rgba(255,255,255,0.02);
    padding: 0.6rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65em;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
}

.matrix-val {
    font-size: 1.8em;
    font-family: 'Teko', sans-serif;
    font-weight: 600;
    line-height: 1;
}

.matrix-label {
    font-size: 0.58em;
    color: var(--muted);
    margin-top: 3px;
    letter-spacing: 0.08em;
}

/* ── RADAR PULSE ── */
.radar-wrap {
    position: relative;
    width: 120px; height: 120px;
    flex-shrink: 0;
}

.radar-wrap svg {
    position: absolute; inset: 0;
    animation: radar-rotate 4s linear infinite;
}

@keyframes radar-rotate {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}

/* ── FOOTER ── */
.hub-footer {
    background: var(--bg2);
    border-top: 1px solid var(--border);
    padding: 2rem 4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68em;
    color: var(--muted);
    flex-wrap: wrap;
    gap: 1rem;
}

.footer-left a  { color: var(--accent); text-decoration: none; }
.footer-right   { text-align: right; }

/* ── ANIMATIONS ── */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
}

@keyframes pulse-border {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0,229,255,0.2); }
    50%       { box-shadow: 0 0 0 4px rgba(0,229,255,0.05); }
}

/* ── STREAMLIT OVERRIDES ── */
.stMarkdown, .stMarkdown p { color: var(--text) !important; }
section[data-testid="stSidebar"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── DATOS LIVE (lee JSONs si existen) ───────────────────────────

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

BASE = os.path.dirname(os.path.abspath(__file__))

# Core — average de actores críticos
core_actors = {
    "Iran/M.Or": load_score(os.path.join(BASE, "..", "SIEG-Core", "data", "geoint_iran_m_oriente.json"), 68),
    "Rusia/Ucr": load_score(os.path.join(BASE, "..", "SIEG-Core", "data", "geoint_rusia_ucrania.json"), 62),
    "China":     load_score(os.path.join(BASE, "..", "SIEG-Core", "data", "geoint_china.json"), 38),
    "N.Korea":   load_score(os.path.join(BASE, "..", "SIEG-Core", "data", "geoint_north_korea.json"), 35),
}
core_score = int(sum(core_actors.values()) / len(core_actors))

# Atlas — average módulos
atlas_modules = {
    "Maritimo":  load_score(os.path.join(BASE, "..", "SIEG-Atlas", "data", "live", "atlas_maritimo.json"), 45),
    "Petroleo":  load_score(os.path.join(BASE, "..", "SIEG-Atlas", "data", "live", "atlas_petroleo.json"), 35),
    "MarChina":  load_score(os.path.join(BASE, "..", "SIEG-Atlas", "data", "live", "atlas_marchina.json"), 42),
    "Ciber":     load_score(os.path.join(BASE, "..", "SIEG-Atlas", "data", "live", "atlas_ciber.json"), 33),
}
atlas_score = int(sum(atlas_modules.values()) / len(atlas_modules))

# Iran
iran_score = int(load_crisis(
    os.path.join(BASE, "..", "SIEG-Iran", "data", "live", "iran_crisis_summary.json"), 65
))

# Global threat index — weighted average
global_score = int(core_score * 0.45 + iran_score * 0.35 + atlas_score * 0.20)


def score_level(s):
    if s >= 80: return ("CRÍTICO",   "#ff3333")
    if s >= 60: return ("ALTO",      "#ff8c00")
    if s >= 40: return ("MEDIO",     "#ffd700")
    return             ("NORMAL",    "#00ff88")

def gauge_html(score, color, size=90):
    r = 35
    circ = 2 * 3.14159 * r
    fill = circ * score / 100
    gap  = circ - fill
    level, _ = score_level(score)
    return f"""
    <div class="gauge-svg-wrap" style="width:{size}px;height:{size}px;">
      <svg viewBox="0 0 90 90" width="{size}" height="{size}">
        <circle cx="45" cy="45" r="{r}" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="6"/>
        <circle cx="45" cy="45" r="{r}" fill="none" stroke="{color}" stroke-width="6"
                stroke-dasharray="{fill:.1f} {gap:.1f}"
                stroke-linecap="round"
                style="filter: drop-shadow(0 0 4px {color})"/>
      </svg>
      <div class="gauge-center">
        <span class="gauge-num" style="color:{color}">{score}</span>
        <span class="gauge-pct">%</span>
      </div>
    </div>"""

def mini_bar(label, value, color):
    return f"""
    <div class="mini-bar-row">
      <span class="mini-bar-label">{label}</span>
      <div class="mini-bar-track">
        <div class="mini-bar-fill" style="width:{value}%;background:{color};box-shadow:0 0 4px {color}40;"></div>
      </div>
      <span class="mini-bar-val">{value}%</span>
    </div>"""

now      = datetime.datetime.now()
now_str  = now.strftime("%d %b %Y · %H:%M UTC")
date_iso = now.strftime("%Y-%m-%d")

# ─── HERO ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hub-hero">
  <div style="max-width:900px">
    <div class="hero-eyebrow">▸ Sistema de Inteligencia Geopolítica · Ecosistema SIEG</div>
    <div class="hero-title">SIEG<span>.</span>HUB</div>
    <div class="hero-subtitle">
      Open Source Intelligence &nbsp;·&nbsp; Early Warning System &nbsp;·&nbsp;
      14 Actores · 6 Ejes · Monitor Iran
    </div>
    <div style="margin-top:1.2rem">
      <span class="hero-badge">OSINT</span>
      <span class="hero-badge">GEOPOLÍTICA</span>
      <span class="hero-badge">INFRAESTRUCTURA</span>
      <span class="hero-live">EN VIVO</span>
    </div>
  </div>
  <div style="position:absolute;right:4rem;top:50%;transform:translateY(-50%);opacity:0.12;
              font-family:'Teko',sans-serif;font-size:12em;font-weight:700;
              color:var(--accent);line-height:1;user-select:none;pointer-events:none;">
    SIEG
  </div>
</div>
""", unsafe_allow_html=True)

# ─── STATUS BAR ──────────────────────────────────────────────────
level_g, color_g = score_level(global_score)
st.markdown(f"""
<div class="status-bar">
  <div class="status-item">
    <div class="status-dot-green"></div>
    <span>Todos los sistemas operativos</span>
  </div>
  <div class="status-item" style="color:var(--text)">
    <span>🕐</span>
    <span class="status-val">{now_str}</span>
  </div>
  <div class="status-item">
    <span>AMENAZA GLOBAL:</span>
    <span class="status-val" style="color:{color_g}">{level_g} · {global_score}%</span>
  </div>
  <div class="status-item">
    <span>CICLO:</span>
    <span class="status-val">60 min · Nodo Odroid-C2</span>
  </div>
  <div style="margin-left:auto;opacity:0.4;font-size:0.9em;">{date_iso}</div>
</div>
""", unsafe_allow_html=True)

# ─── CARDS GRID ──────────────────────────────────────────────────
core_level,  core_color  = score_level(core_score)
atlas_level, atlas_color = score_level(atlas_score)
iran_level,  iran_color  = score_level(iran_score)

core_bars  = "".join(mini_bar(k, int(v), core_color)  for k, v in core_actors.items())
atlas_bars = "".join(mini_bar(k, int(v), atlas_color) for k, v in atlas_modules.items())

iran_vectors = {
    "Conflicto":  load_score(os.path.join(BASE, "..", "SIEG-Iran", "data", "live", "iran_conflicto_directo.json"), 72),
    "Nuclear":    load_score(os.path.join(BASE, "..", "SIEG-Iran", "data", "live", "iran_nuclear.json"), 68),
    "Proxies":    load_score(os.path.join(BASE, "..", "SIEG-Iran", "data", "live", "iran_proxies_regionales.json"), 70),
    "Hormuz":     load_score(os.path.join(BASE, "..", "SIEG-Iran", "data", "live", "iran_energia_hormuz.json"), 65),
}
iran_bars = "".join(mini_bar(k, int(v), iran_color) for k, v in iran_vectors.items())

st.markdown(f"""
<div class="main-grid">

  <!-- ── SIEG CORE ── -->
  <div class="module-card card-core">
    <div class="card-inner">
      <div class="card-tag tag-core">▸ Módulo 01 · Geopolítica Global</div>
      <div class="card-title">SIEG CORE</div>
      <div class="card-desc">Motor principal de análisis. 14 actores geopolíticos, 3 capas de fuentes OSINT, autolearning y detección de disonancia narrativa.</div>

      <div class="gauge-wrap">
        {gauge_html(core_score, core_color)}
        <div class="gauge-info">
          <div class="gauge-label">Índice de tensión</div>
          <div class="gauge-level" style="color:{core_color}">{core_level}</div>
          <div class="gauge-actors">14 actores · Ciclo 60 min</div>
        </div>
      </div>

      <div class="mini-bars">{core_bars}</div>

      <a class="cta-btn btn-core" href="https://sieg-intelligence-radar.streamlit.app/" target="_blank">
        Acceder a SIEG Core
      </a>
    </div>
  </div>

  <!-- ── SIEG ATLAS ── -->
  <div class="module-card card-atlas">
    <div class="card-inner">
      <div class="card-tag tag-atlas">▸ Módulo 02 · Infraestructura Crítica</div>
      <div class="card-title">SIEG ATLAS</div>
      <div class="card-desc">Monitorización de infraestructura crítica global: energía, rutas marítimas, cables submarinos, espacio orbital y ciberespacio.</div>

      <div class="gauge-wrap">
        {gauge_html(atlas_score, atlas_color)}
        <div class="gauge-info">
          <div class="gauge-label">Índice de riesgo</div>
          <div class="gauge-level" style="color:{atlas_color}">{atlas_level}</div>
          <div class="gauge-actors">6 ejes · Ciclo 60 min</div>
        </div>
      </div>

      <div class="mini-bars">{atlas_bars}</div>

      <a class="cta-btn btn-atlas" href="https://sieg-atlas-intelligence.streamlit.app/" target="_blank">
        Acceder a SIEG Atlas
      </a>
    </div>
  </div>

  <!-- ── SIEG IRAN ── -->
  <div class="module-card card-iran">
    <div class="card-inner">
      <div class="card-tag tag-iran">▸ Módulo 03 · Sala de Crisis</div>
      <div class="card-title">SIEG IRAN</div>
      <div class="card-desc">Monitor especializado en el conflicto Iran-Israel. 8 vectores de análisis: nuclear, proxies, Hormuz, teatro regional y posición global.</div>

      <div class="gauge-wrap">
        {gauge_html(iran_score, iran_color)}
        <div class="gauge-info">
          <div class="gauge-label">Índice de crisis</div>
          <div class="gauge-level" style="color:{iran_color}">{iran_level}</div>
          <div class="gauge-actors">8 vectores · Ciclo 60 min</div>
        </div>
      </div>

      <div class="mini-bars">{iran_bars}</div>

      <a class="cta-btn btn-iran" href="https://sieg-iran-crisis.streamlit.app/" target="_blank">
        Acceder a SIEG Iran
      </a>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ─── GLOBAL THREAT PANEL ─────────────────────────────────────────
total_actors = 14 + 6 + 8
n_high_core  = sum(1 for v in core_actors.values()  if v >= 60)
n_high_atlas = sum(1 for v in atlas_modules.values() if v >= 50)
n_high_iran  = sum(1 for v in iran_vectors.values()  if v >= 60)
n_high_total = n_high_core + n_high_atlas + n_high_iran

st.markdown(f"""
<div class="global-panel">
  <div class="panel-title">◈ Matriz de Amenaza Global</div>

  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
              background:var(--border);border:1px solid var(--border);
              border-radius:3px;overflow:hidden;margin-bottom:1.8rem;">
    <div style="background:var(--bg3);padding:1.2rem;text-align:center;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.6em;color:var(--muted);letter-spacing:0.12em;margin-bottom:0.5rem;">ÍNDICE GLOBAL</div>
      <div style="font-family:'Teko',sans-serif;font-size:2.8em;font-weight:600;color:{color_g};line-height:1;text-shadow:0 0 20px {color_g}40">{global_score}%</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:{color_g};margin-top:4px;">{level_g}</div>
    </div>
    <div style="background:var(--bg3);padding:1.2rem;text-align:center;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.6em;color:var(--muted);letter-spacing:0.12em;margin-bottom:0.5rem;">VECTORES ACTIVOS</div>
      <div style="font-family:'Teko',sans-serif;font-size:2.8em;font-weight:600;color:#ff8c00;line-height:1;">{total_actors}</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:var(--muted);margin-top:4px;">monitorizados</div>
    </div>
    <div style="background:var(--bg3);padding:1.2rem;text-align:center;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.6em;color:var(--muted);letter-spacing:0.12em;margin-bottom:0.5rem;">EN ALERTA</div>
      <div style="font-family:'Teko',sans-serif;font-size:2.8em;font-weight:600;color:#ff3333;line-height:1;">{n_high_total}</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:var(--muted);margin-top:4px;">score ≥ 60%</div>
    </div>
    <div style="background:var(--bg3);padding:1.2rem;text-align:center;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.6em;color:var(--muted);letter-spacing:0.12em;margin-bottom:0.5rem;">FUENTES OSINT</div>
      <div style="font-family:'Teko',sans-serif;font-size:2.8em;font-weight:600;color:var(--accent);line-height:1;">120+</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:var(--muted);margin-top:4px;">RSS · autolearning</div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;">

    <div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.65em;color:var(--muted);
                  letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.8rem;">
        Metodología
      </div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:0.9em;color:#4a6a8a;line-height:1.7;">
        Análisis OSINT multi-fuente · Scoring léxico ponderado por CF (Coeficiente de Fiabilidad) ·
        Autolearning 3 capas (primarias → fallback → Google News) ·
        Detección de disonancia narrativa · Suelos dinámicos por actor ·
        Flash News: extracción automática de eventos críticos (TTL 48h)
      </div>
    </div>

    <div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.65em;color:var(--muted);
                  letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.8rem;">
        Infraestructura
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.68em;color:#3a5a7a;line-height:2;">
        <span style="color:var(--accent)">■</span> Nodo físico: Odroid-C2 ARM · DietPi v9.x<br>
        <span style="color:var(--accent)">■</span> Ciclo: 60 min · Git sync automático<br>
        <span style="color:var(--accent)">■</span> Scanners: Core V9.3 · Atlas V1.3 · Iran V1.1<br>
        <span style="color:var(--accent)">■</span> Dashboards: Streamlit Cloud · Acceso público
      </div>
    </div>

  </div>
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────
year = now.year
st.markdown(f"""
<div class="hub-footer">
  <div class="footer-left">
    🛡 <strong style="color:var(--text)">SIEG Intelligence Hub</strong> &nbsp;·&nbsp;
    Sistema de Inteligencia de Eventos Geopolíticos &nbsp;·&nbsp;
    © {year} <strong>M. Castillo</strong> &nbsp;·&nbsp;
    <a href="mailto:mybloggingnotes@gmail.com">mybloggingnotes@gmail.com</a>
  </div>
  <div class="footer-right" style="color:var(--muted)">
    Datos de fuentes abiertas (OSINT) &nbsp;·&nbsp; Solo uso informativo &nbsp;·&nbsp;
    Actualizado: {now_str}
  </div>
</div>
""", unsafe_allow_html=True)
