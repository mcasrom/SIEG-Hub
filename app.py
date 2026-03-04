"""
SIEG Hub — Portal Central V2.2
Novedades vs V2.1:
  - Tab "🔍 Auditoría" con 5 bloques:
    1. Estado del sistema (timestamps, sistema no parado)
    2. Cobertura de noticias por actor/vector vs umbral mínimo
    3. Credibilidad CF promedio + comparativa tier-1
    4. Ratio capas (primarias / fallback / web)
    5. Detección de scores anómalos o congelados
"""

import streamlit as st
import datetime
import json
import os
import math
import glob

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

.stApp::before {
    content:''; position:fixed; top:0; left:0; right:0; bottom:0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 3px,
        rgba(0,229,255,0.010) 3px, rgba(0,229,255,0.010) 4px
    );
    pointer-events:none; z-index:9999;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-bottom: 2px solid var(--border) !important;
    padding: 0 4rem !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75em !important;
    letter-spacing: 0.1em !important;
    color: var(--muted) !important;
    padding: 0.8rem 1.4rem !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 0 !important;
    background: var(--bg) !important;
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
}
.hub-hero::after {
    content:''; position:absolute; bottom:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent 0%, var(--accent) 30%, var(--accent) 70%, transparent 100%);
    opacity:0.35;
}
.hero-eyebrow { font-family:'Share Tech Mono',monospace; font-size:0.72em; color:var(--accent); letter-spacing:0.3em; opacity:0.65; margin-bottom:0.6rem; }
.hero-title   { font-family:'Teko',sans-serif; font-size:5em; font-weight:600; line-height:0.92; color:#fff; text-shadow:0 0 80px rgba(0,229,255,0.18); }
.hero-title span { color:var(--accent); }
.hero-sub     { font-family:'Share Tech Mono',monospace; font-size:0.84em; color:#5a7090; margin-top:0.9rem; letter-spacing:0.07em; }
.hero-badge   { display:inline-block; background:rgba(0,229,255,0.07); border:1px solid rgba(0,229,255,0.22); color:var(--accent); font-family:'Share Tech Mono',monospace; font-size:0.65em; padding:3px 10px; border-radius:2px; letter-spacing:0.15em; margin-right:6px; margin-top:1rem; }
.hero-live    { display:inline-block; background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.28); color:var(--green); font-family:'Share Tech Mono',monospace; font-size:0.65em; padding:3px 10px; border-radius:2px; letter-spacing:0.15em; margin-top:1rem; animation:livepulse 2s ease infinite; }
.hero-watermark { position:absolute; right:3rem; top:50%; transform:translateY(-50%); font-family:'Teko',sans-serif; font-size:11em; font-weight:700; color:rgba(0,229,255,0.04); line-height:1; user-select:none; pointer-events:none; }

/* ── STATUS BAR ── */
.status-bar { background:var(--bg2); border-bottom:1px solid var(--border); padding:0.65rem 4rem; font-family:'Share Tech Mono',monospace; font-size:0.70em; color:var(--muted); display:flex; align-items:center; gap:2rem; flex-wrap:wrap; }
.sdot-g { display:inline-block; width:6px; height:6px; border-radius:50%; background:var(--green); box-shadow:0 0 5px var(--green); margin-right:5px; animation:blink 2s ease infinite; }
.sval { color:var(--text); font-weight:bold; }

/* ── TAB CONTENT WRAPPER ── */
.tab-body { padding: 2rem 4rem 3rem; }

/* ── MODULE CARD ── */
.mod-card { background:var(--bg2); border:1px solid var(--border); border-radius:4px; position:relative; overflow:hidden; transition:transform 0.25s, box-shadow 0.25s, border-color 0.25s; height:100%; }
.mod-card:hover { transform:translateY(-4px); }
.mod-card-body { padding:1.6rem 1.8rem 1.8rem; }
.mod-tag   { font-family:'Share Tech Mono',monospace; font-size:0.60em; letter-spacing:0.22em; text-transform:uppercase; opacity:0.55; margin-bottom:0.7rem; }
.mod-title { font-family:'Teko',sans-serif; font-size:2.5em; font-weight:500; line-height:1; color:#fff; margin-bottom:0.4rem; }
.mod-desc  { font-family:'Rajdhani',sans-serif; font-size:0.90em; color:#4a5e78; line-height:1.55; margin-bottom:1.3rem; min-height:2.8rem; }

/* ── GAUGE ── */
.gauge-row { display:flex; align-items:center; gap:1rem; background:rgba(0,0,0,0.28); border:1px solid var(--border); border-radius:3px; padding:0.9rem 1rem; margin-bottom:1.1rem; }
.gsvg { position:relative; width:86px; height:86px; flex-shrink:0; }
.gsvg svg { width:86px; height:86px; transform:rotate(-90deg); }
.gcenter { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:'Teko',sans-serif; }
.gnum { font-size:1.55em; font-weight:600; line-height:1; }
.gpct { font-size:0.52em; opacity:0.55; letter-spacing:0.1em; }
.ginfo { flex:1; }
.glabel   { font-family:'Share Tech Mono',monospace; font-size:0.60em; color:var(--muted); letter-spacing:0.12em; text-transform:uppercase; }
.glevel   { font-family:'Rajdhani',sans-serif; font-size:1.05em; font-weight:600; margin-top:3px; }
.gactors  { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); margin-top:5px; }

/* ── MINI BARS ── */
.mbars { margin-bottom:1.3rem; }
.mrow  { display:flex; align-items:center; gap:7px; margin-bottom:5px; }
.mlbl  { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); width:72px; flex-shrink:0; }
.mtrack { flex:1; height:3px; background:rgba(255,255,255,0.05); border-radius:2px; overflow:hidden; }
.mfill  { height:100%; border-radius:2px; }
.mval   { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); width:26px; text-align:right; flex-shrink:0; }

/* ── CTA ── */
.cta { display:block; text-align:center; text-decoration:none !important; padding:0.65rem 1rem; border-radius:2px; font-family:'Share Tech Mono',monospace; font-size:0.70em; letter-spacing:0.14em; text-transform:uppercase; font-weight:bold; transition:filter 0.2s; }
.cta:hover { filter:brightness(1.4); }
.cta::after { content:' →'; }
.cta-g { background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.35); color:var(--green) !important; }
.cta-b { background:rgba(0,229,255,0.07); border:1px solid rgba(0,229,255,0.35); color:var(--accent) !important; }
.cta-r { background:rgba(255,51,51,0.07);  border:1px solid rgba(255,51,51,0.35);  color:var(--red) !important; }

/* ── GLOBAL PANEL ── */
.gpanel { background:var(--bg2); border:1px solid var(--border); border-radius:4px; padding:2rem 2.5rem; margin:1.5rem 0 0; }
.gpanel-title { font-family:'Teko',sans-serif; font-size:1.4em; color:var(--gold); letter-spacing:0.12em; text-transform:uppercase; border-bottom:1px solid var(--border); padding-bottom:0.7rem; margin-bottom:1.3rem; }
.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--border); border:1px solid var(--border); border-radius:3px; overflow:hidden; margin-bottom:1.5rem; }
.kpi-cell { background:var(--bg3); padding:1.1rem; text-align:center; }
.kpi-lbl { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); letter-spacing:0.12em; margin-bottom:0.4rem; }
.kpi-val { font-family:'Teko',sans-serif; font-size:2.6em; font-weight:600; line-height:1; }
.kpi-sub { font-family:'Share Tech Mono',monospace; font-size:0.58em; color:var(--muted); margin-top:3px; }
.info-grid { display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; }
.info-head { font-family:'Share Tech Mono',monospace; font-size:0.62em; color:var(--muted); letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.7rem; }
.info-body { font-family:'Rajdhani',sans-serif; font-size:0.88em; color:#3a5070; line-height:1.75; }
.info-mono { font-family:'Share Tech Mono',monospace; font-size:0.66em; color:#2a4060; line-height:2.0; }
.info-mono span { color:var(--accent); }

/* ── AUDIT SPECIFIC ── */
.audit-section {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: 4px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;
}
.audit-title {
    font-family: 'Teko', sans-serif; font-size: 1.3em;
    color: var(--accent); letter-spacing: 0.12em; text-transform: uppercase;
    border-bottom: 1px solid var(--border); padding-bottom: 0.6rem; margin-bottom: 1.2rem;
}
.audit-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.55rem 0; border-bottom: 1px solid rgba(26,37,64,0.6);
    font-family: 'Share Tech Mono', monospace; font-size: 0.72em;
}
.audit-row:last-child { border-bottom: none; }
.audit-key   { color: var(--muted); width: 160px; flex-shrink: 0; }
.audit-val   { color: var(--text); flex: 1; }
.audit-badge {
    display: inline-block; font-family: 'Share Tech Mono', monospace;
    font-size: 0.85em; padding: 2px 9px; border-radius: 2px;
    font-weight: bold; letter-spacing: 0.1em;
}
.badge-ok   { background: rgba(0,255,136,0.08); border:1px solid rgba(0,255,136,0.3); color:#00ff88; }
.badge-warn { background: rgba(255,140,0,0.08);  border:1px solid rgba(255,140,0,0.3);  color:#ff8c00; }
.badge-err  { background: rgba(255,51,51,0.08);  border:1px solid rgba(255,51,51,0.3);  color:#ff3333; }
.badge-info { background: rgba(0,229,255,0.08);  border:1px solid rgba(0,229,255,0.3);  color:#00e5ff; }

/* coverage bar */
.cov-bar-wrap { display:flex; align-items:center; gap:8px; }
.cov-track    { flex:1; height:5px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden; }
.cov-fill     { height:100%; border-radius:3px; }
.cov-lbl      { font-family:'Share Tech Mono',monospace; font-size:0.62em; color:var(--muted); width:200px; flex-shrink:0; }
.cov-val      { font-family:'Share Tech Mono',monospace; font-size:0.62em; width:36px; text-align:right; }

/* CF tiers */
.tier-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.tier-name { font-family:'Share Tech Mono',monospace; font-size:0.62em; color:var(--muted); width:120px; }
.tier-bar  { flex:1; height:6px; border-radius:3px; }
.tier-cf   { font-family:'Teko',sans-serif; font-size:1.1em; font-weight:600; width:50px; text-align:right; }
.tier-badge{ font-family:'Share Tech Mono',monospace; font-size:0.58em; padding:2px 6px; border-radius:2px; }

/* anomaly pill */
.anomaly-ok   { font-family:'Share Tech Mono',monospace; font-size:0.68em; color:#00ff88; }
.anomaly-warn { font-family:'Share Tech Mono',monospace; font-size:0.68em; color:#ff8c00; animation:blink 2s ease infinite; }
.anomaly-err  { font-family:'Share Tech Mono',monospace; font-size:0.68em; color:#ff3333; animation:blink 1s ease infinite; }

/* ── FOOTER ── */
.hub-footer { background:var(--bg2); border-top:1px solid var(--border); padding:1.8rem 4rem; margin-top:2rem; display:flex; justify-content:space-between; align-items:center; font-family:'Share Tech Mono',monospace; font-size:0.66em; color:var(--muted); flex-wrap:wrap; gap:1rem; }
.hub-footer a { color:var(--accent); text-decoration:none; }

/* ── ANIMATIONS ── */
@keyframes blink     { 0%,100%{opacity:1} 50%{opacity:0.15} }
@keyframes livepulse { 0%,100%{opacity:1} 50%{opacity:0.6}  }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ─────────────────────────────────────────────────────

def load_json(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}

def load_score(path: str, default: float = 45.0) -> float:
    return float(load_json(path).get("score", default))

def load_crisis(path: str, default: float = 65.0) -> float:
    return float(load_json(path).get("crisis_score", default))

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
        f'</div></div>'
    )

def build_bars(items: dict, color: str) -> str:
    html = '<div class="mbars">'
    for label, val in items.items():
        v = int(val)
        html += (f'<div class="mrow"><span class="mlbl">{label}</span>'
                 f'<div class="mtrack"><div class="mfill" style="width:{v}%;background:{color};'
                 f'box-shadow:0 0 4px {color}55;"></div></div>'
                 f'<span class="mval">{v}%</span></div>')
    return html + '</div>'

def build_card(card_class, top_gradient, tag_color, tag_text,
               title, desc, score, items, gauge_label, gauge_actors,
               cta_class, cta_url, cta_text) -> str:
    level, color = score_level(score)
    return f"""
<div class="mod-card {card_class}" style="border-top:3px solid {top_gradient[0]};">
  <div style="height:3px;background:linear-gradient(90deg,{top_gradient[0]},{top_gradient[1]});"></div>
  <div class="mod-card-body">
    <div class="mod-tag" style="color:{tag_color};">▸ {tag_text}</div>
    <div class="mod-title">{title}</div>
    <div class="mod-desc">{desc}</div>
    <div class="gauge-row">
      {build_gauge(score, color)}
      <div class="ginfo">
        <div class="glabel">{gauge_label}</div>
        <div class="glevel" style="color:{color};">{level}</div>
        <div class="gactors">{gauge_actors}</div>
      </div>
    </div>
    {build_bars(items, color)}
    <a class="cta {cta_class}" href="{cta_url}" target="_blank">{cta_text}</a>
  </div>
</div>"""

def badge(text, cls):
    return f'<span class="audit-badge badge-{cls}">{text}</span>'

def ts_age(ts: float, now_ts: float) -> tuple:
    """Returns (age_str, status_class)"""
    mins = int((now_ts - ts) / 60) if ts > 0 else 9999
    if mins < 75:   return f"hace {mins} min", "ok"
    if mins < 180:  return f"hace {mins//60}h {mins%60}min", "warn"
    if mins < 1440: return f"hace {mins//60}h", "err"
    return f"hace {mins//1440}d", "err"

def cov_bar(label, value, min_val, max_val=200):
    pct   = min(int(value / max_val * 100), 100)
    color = "#00ff88" if value >= min_val else ("#ff8c00" if value >= min_val * 0.6 else "#ff3333")
    ok    = "ok" if value >= min_val else ("warn" if value >= min_val * 0.6 else "err")
    return (
        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:7px;">'
        f'<span class="cov-lbl">{label}</span>'
        f'<div class="cov-track"><div class="cov-fill" style="width:{pct}%;background:{color};box-shadow:0 0 4px {color}44;"></div></div>'
        f'<span class="cov-val" style="color:{color};">{int(value)}</span>'
        f'<span class="audit-badge badge-{ok}" style="font-size:0.6em;padding:1px 6px;">{"OK" if ok=="ok" else "BAJO" if ok=="warn" else "CRÍTICO"}</span>'
        f'</div>'
    )

def cf_tier_bar(name, cf_val, ref_val, color, tier_label):
    pct     = int(cf_val * 100)
    ref_pct = int(ref_val * 100)
    diff    = cf_val - ref_val
    diff_color = "#00ff88" if diff >= 0 else "#ff8c00"
    diff_str   = f"+{diff:.2f}" if diff >= 0 else f"{diff:.2f}"
    return (
        f'<div class="tier-row">'
        f'<span class="tier-name">{name}</span>'
        f'<div class="tier-bar" style="flex:1;height:6px;background:rgba(255,255,255,0.04);border-radius:3px;overflow:hidden;position:relative;">'
        f'<div style="height:100%;width:{ref_pct}%;background:rgba(255,255,255,0.12);position:absolute;top:0;left:0;"></div>'
        f'<div style="height:100%;width:{pct}%;background:{color};box-shadow:0 0 4px {color}55;position:absolute;top:0;left:0;border-radius:3px;"></div>'
        f'</div>'
        f'<span class="tier-cf" style="color:{color};">{cf_val:.2f}</span>'
        f'<span class="tier-badge" style="background:rgba(0,0,0,0.3);color:{diff_color};border:1px solid {diff_color}44;">{diff_str} vs T1</span>'
        f'</div>'
    )


# ─── DATOS ───────────────────────────────────────────────────────

BASE = os.path.dirname(os.path.abspath(__file__))
# En Streamlit Cloud los JSONs están en data/ dentro del propio repo SIEG-Hub
# El crontab del Odroid debe copiarlos aquí antes del git push
C    = os.path.join(BASE, "data", "core")
A    = os.path.join(BASE, "data", "atlas")
I    = os.path.join(BASE, "data", "iran")

now    = datetime.datetime.now()
now_ts = now.timestamp()

# Cargar todos los JSONs completos (para auditoría)
core_files = {
    "Iran_M_Oriente":  load_json(os.path.join(C, "geoint_iran_m_oriente.json")),
    "Rusia_Ucrania":   load_json(os.path.join(C, "geoint_rusia_ucrania.json")),
    "USA":             load_json(os.path.join(C, "geoint_usa.json")),
    "China":           load_json(os.path.join(C, "geoint_china.json")),
    "North_Korea":     load_json(os.path.join(C, "geoint_north_korea.json")),
    "Sahel":           load_json(os.path.join(C, "geoint_sahel.json")),
    "Europa_Core":     load_json(os.path.join(C, "geoint_europa_core.json")),
    "Asia_Pacifico":   load_json(os.path.join(C, "geoint_asia_pacifico.json")),
    "Espana":          load_json(os.path.join(C, "geoint_espana.json")),
    "Latam":           load_json(os.path.join(C, "geoint_latam.json")),
    "Mexico":          load_json(os.path.join(C, "geoint_mexico.json")),
    "Argentina":       load_json(os.path.join(C, "geoint_argentina.json")),
    "Brasil":          load_json(os.path.join(C, "geoint_brasil.json")),
    "Australia":       load_json(os.path.join(C, "geoint_australia.json")),
}
atlas_files = {
    "Petroleo":  load_json(os.path.join(A, "atlas_petroleo.json")),
    "Maritimo":  load_json(os.path.join(A, "atlas_maritimo.json")),
    "Cables":    load_json(os.path.join(A, "atlas_cables.json")),
    "MarChina":  load_json(os.path.join(A, "atlas_marchina.json")),
    "Espacio":   load_json(os.path.join(A, "atlas_espacio.json")),
    "Ciber":     load_json(os.path.join(A, "atlas_ciber.json")),
}
iran_files = {
    "Conflicto_Directo":  load_json(os.path.join(I, "iran_conflicto_directo.json")),
    "Proxies_Regionales": load_json(os.path.join(I, "iran_proxies_regionales.json")),
    "Nuclear":            load_json(os.path.join(I, "iran_nuclear.json")),
    "Energia_Hormuz":     load_json(os.path.join(I, "iran_energia_hormuz.json")),
    "Teatro_Regional":    load_json(os.path.join(I, "iran_teatro_regional.json")),
    "Posicion_Global":    load_json(os.path.join(I, "iran_posicion_global.json")),
    "Sanciones_Economia": load_json(os.path.join(I, "iran_sanciones_economia.json")),
    "Diplomatico":        load_json(os.path.join(I, "iran_diplomatico.json")),
}

def get_noticias(data: dict) -> float:
    """Core usa 'noticias_procesadas', Atlas/Iran usan 'noticias'."""
    return float(data.get("noticias_procesadas") or data.get("noticias") or 0)

# Scores para las cards de la tab 1
core_actors  = {k: float(v.get("score", 45)) for k, v in list(core_files.items())[:4]}
atlas_modules= {k: float(v.get("score", 35)) for k, v in atlas_files.items()}
iran_vectors = {
    "Conflicto": float(iran_files["Conflicto_Directo"].get("score",  72)),
    "Nuclear":   float(iran_files["Nuclear"].get("score",            68)),
    "Proxies":   float(iran_files["Proxies_Regionales"].get("score", 70)),
    "Hormuz":    float(iran_files["Energia_Hormuz"].get("score",     65)),
}

core_score   = int(sum(core_actors.values())   / len(core_actors))
atlas_score  = int(sum(atlas_modules.values()) / len(atlas_modules))
iran_score   = int(load_crisis(os.path.join(I, "iran_crisis_summary.json"), 65))
global_score = int(core_score * 0.45 + iran_score * 0.35 + atlas_score * 0.20)
gl_level, gl_color = score_level(global_score)
n_alert = (sum(1 for v in core_actors.values()  if v >= 60) +
           sum(1 for v in atlas_modules.values() if v >= 50) +
           sum(1 for v in iran_vectors.values()  if v >= 60))
now_str = now.strftime("%d %b %Y · %H:%M UTC")

# ─── CF Tier-1 de referencia (fuentes internacionales no polarizadas) ─
# CF asignado en mapa_fuentes / atlas a las tier-1
TIER1_CF = {
    "BBC World":      0.90, "Reuters":    0.92, "NYT":   0.90,
    "Foreign Policy": 0.90, "Al Jazeera": 0.70, "AP":    0.90,
    "The Diplomat":   0.80, "Nikkei Asia":0.80,
}
TIER1_AVG = round(sum(TIER1_CF.values()) / len(TIER1_CF), 2)  # ~0.865


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

# ─── TABS ────────────────────────────────────────────────────────
tab_hub, tab_audit = st.tabs([
    "🛡  SIEG HUB",
    "🔍  AUDITORÍA DEL SISTEMA",
])


# ════════════════════════════════════════════════════════════════
# TAB 1 — HUB PRINCIPAL
# ════════════════════════════════════════════════════════════════
with tab_hub:
    st.markdown("<div class='tab-body'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(build_card(
            "card-core", ("#00ff88","#00aa55"), "#00ff88",
            "Módulo 01 · Geopolítica Global", "SIEG CORE",
            "Motor principal. 14 actores geopolíticos, 3 capas OSINT, autolearning y detección de disonancia narrativa.",
            core_score, core_actors, "Índice de tensión", "14 actores · Ciclo 60 min",
            "cta-g", "https://sieg-intelligence-radar.streamlit.app/", "Acceder a SIEG Core",
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(build_card(
            "card-atlas", ("#00e5ff","#0077aa"), "#00e5ff",
            "Módulo 02 · Infraestructura Crítica", "SIEG ATLAS",
            "6 ejes de infraestructura crítica: energía, rutas marítimas, cables submarinos, espacio y ciberespacio.",
            atlas_score, atlas_modules, "Índice de riesgo", "6 ejes · Ciclo 60 min",
            "cta-b", "https://sieg-atlas-intelligence.streamlit.app/", "Acceder a SIEG Atlas",
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(build_card(
            "card-iran", ("#ff3333","#aa2200"), "#ff3333",
            "Módulo 03 · Sala de Crisis", "SIEG IRAN",
            "Monitor Iran-Israel. 8 vectores: nuclear, proxies, Hormuz, teatro regional y posición de potencias.",
            iran_score, iran_vectors, "Índice de crisis", "8 vectores · Ciclo 60 min",
            "cta-r", "https://sieg-iran-crisis.streamlit.app/", "Acceder a SIEG Iran",
        ), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="gpanel" style="margin-top:2rem;">
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

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 2 — AUDITORÍA DEL SISTEMA
# ════════════════════════════════════════════════════════════════
with tab_audit:
    st.markdown("<div class='tab-body'>", unsafe_allow_html=True)

    # ── Cabecera auditoría ───────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Teko',sans-serif;font-size:2em;color:#00e5ff;letter-spacing:0.1em;">
        🔍 PANEL DE AUDITORÍA — INTEGRIDAD DEL SISTEMA
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.70em;color:#3a4a6a;margin-top:4px;">
        Verificación automática · Actividad de scanners · Cobertura de fuentes · Credibilidad CF · Detección de anomalías
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # BLOQUE 1 — ESTADO DEL SISTEMA (timestamps)
    # ════════════════════════════════════════════════════════════
    all_systems = {
        "SIEG Core":  core_files,
        "SIEG Atlas": atlas_files,
        "SIEG Iran":  iran_files,
    }

    for sys_name, sys_files in all_systems.items():
        timestamps = [float(d.get("timestamp", 0)) for d in sys_files.values() if d.get("timestamp", 0) > 0]
        if timestamps:
            last_ts  = max(timestamps)
            age_str, age_cls = ts_age(last_ts, now_ts)
            last_dt  = datetime.datetime.fromtimestamp(last_ts).strftime("%d/%m/%Y %H:%M:%S")
            n_fresh  = sum(1 for ts in timestamps if (now_ts - ts) < 4500)  # < 75 min
            n_stale  = len(timestamps) - n_fresh
        else:
            last_dt, age_str, age_cls = "SIN DATOS", "desconocido", "err"
            n_fresh, n_stale = 0, len(sys_files)

        sys_color = {"SIEG Core": "#00ff88", "SIEG Atlas": "#00e5ff", "SIEG Iran": "#ff3333"}[sys_name]

        ts_rows = ""
        for actor, data in sys_files.items():
            ts_a = float(data.get("timestamp", 0))
            if ts_a > 0:
                a_str, a_cls = ts_age(ts_a, now_ts)
                dt_str = datetime.datetime.fromtimestamp(ts_a).strftime("%H:%M:%S")
                ver    = data.get("version", "?")
                ts_rows += (
                    f'<div class="audit-row">'
                    f'<span class="audit-key">{actor.replace("_"," ")[:20]}</span>'
                    f'<span class="audit-val">{dt_str}</span>'
                    f'<span class="audit-val anomaly-{a_cls}">{a_str}</span>'
                    f'<span class="audit-badge badge-info" style="font-size:0.7em;">{ver}</span>'
                    f'</div>'
                )
            else:
                ts_rows += (
                    f'<div class="audit-row">'
                    f'<span class="audit-key">{actor.replace("_"," ")[:20]}</span>'
                    f'<span class="audit-val" style="color:#ff3333;">SIN DATOS</span>'
                    f'<span>{badge("OFFLINE", "err")}</span>'
                    f'</div>'
                )

        st.markdown(f"""
        <div class="audit-section" style="border-left:3px solid {sys_color};">
          <div class="audit-title" style="color:{sys_color};">
            ◈ {sys_name} — Estado de Actividad
            &nbsp;&nbsp;
            {badge("ACTIVO" if age_cls=="ok" else "RETRASADO" if age_cls=="warn" else "PARADO", age_cls)}
            &nbsp;
            {badge(f"Último scan: {age_str}", age_cls)}
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1rem;">
            <div style="background:rgba(0,0,0,0.2);border:1px solid var(--border);border-radius:3px;padding:0.8rem;text-align:center;">
              <div class="kpi-lbl">ÚLTIMA SEÑAL</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.75em;color:var(--text);margin-top:4px;">{last_dt}</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border:1px solid var(--border);border-radius:3px;padding:0.8rem;text-align:center;">
              <div class="kpi-lbl">VECTORES FRESCOS</div>
              <div style="font-family:'Teko',sans-serif;font-size:1.8em;color:#00ff88;line-height:1;">{n_fresh}</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border:1px solid var(--border);border-radius:3px;padding:0.8rem;text-align:center;">
              <div class="kpi-lbl">VECTORES RETRASADOS</div>
              <div style="font-family:'Teko',sans-serif;font-size:1.8em;color:{'#00ff88' if n_stale==0 else '#ff8c00'};line-height:1;">{n_stale}</div>
            </div>
          </div>
          <details>
            <summary style="font-family:'Share Tech Mono',monospace;font-size:0.68em;color:var(--muted);cursor:pointer;margin-bottom:0.6rem;">
              ▸ Ver detalle por actor/vector
            </summary>
            {ts_rows}
          </details>
        </div>
        """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # BLOQUE 2 — COBERTURA DE NOTICIAS
    # ════════════════════════════════════════════════════════════
    MIN_CORE  = 60
    MIN_ATLAS = 40
    MIN_IRAN  = 40

    cov_core  = "".join(
        cov_bar(k.replace("_"," ")[:22], get_noticias(v), MIN_CORE)
        for k, v in core_files.items()
    )
    cov_atlas = "".join(
        cov_bar(k, get_noticias(v), MIN_ATLAS)
        for k, v in atlas_files.items()
    )
    cov_iran  = "".join(
        cov_bar(k.replace("_"," ")[:22], get_noticias(v), MIN_IRAN)
        for k, v in iran_files.items()
    )

    total_noticias = (
        sum(get_noticias(v) for v in core_files.values()) +
        sum(get_noticias(v) for v in atlas_files.values()) +
        sum(get_noticias(v) for v in iran_files.values())
    )
    n_bajo_umbral = (
        sum(1 for v in core_files.values()  if get_noticias(v) < MIN_CORE)  +
        sum(1 for v in atlas_files.values() if get_noticias(v) < MIN_ATLAS) +
        sum(1 for v in iran_files.values()  if get_noticias(v) < MIN_IRAN)
    )

    st.markdown(f"""
    <div class="audit-section" style="border-left:3px solid #ffd700;">
      <div class="audit-title" style="color:#ffd700;">
        ◈ Cobertura de Noticias — Vectores vs Umbral Mínimo
        &nbsp;&nbsp;
        {badge(f"Total: {int(total_noticias)} noticias", "info")}
        &nbsp;
        {badge(f"{n_bajo_umbral} bajo umbral", "warn" if n_bajo_umbral > 0 else "ok")}
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:2rem;">
        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:#00ff88;
                      letter-spacing:0.15em;margin-bottom:0.8rem;">
            CORE — umbral {MIN_CORE} items
          </div>
          {cov_core}
        </div>
        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:#00e5ff;
                      letter-spacing:0.15em;margin-bottom:0.8rem;">
            ATLAS — umbral {MIN_ATLAS} items
          </div>
          {cov_atlas}
        </div>
        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:#ff3333;
                      letter-spacing:0.15em;margin-bottom:0.8rem;">
            IRAN — umbral {MIN_IRAN} items
          </div>
          {cov_iran}
        </div>
      </div>

      <div style="font-family:'Share Tech Mono',monospace;font-size:0.60em;color:var(--muted);
                  margin-top:1rem;padding-top:0.8rem;border-top:1px solid var(--border);">
        Barra gris = umbral mínimo · Verde ≥ umbral · Naranja ≥ 60% umbral · Rojo &lt; 60% umbral
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # BLOQUE 3 — CREDIBILIDAD CF vs TIER-1
    # ════════════════════════════════════════════════════════════

    # CF promedio real de cada sistema (extraído de JSONs)
    def avg_cf(files_dict, field="cf_promedio"):
        vals = [float(v.get(field, 0)) for v in files_dict.values() if v.get(field, 0) > 0]
        # Si no hay campo cf_promedio, estimar por uso_fallback y uso_web
        if not vals:
            cfs = []
            for v in files_dict.values():
                if v.get("uso_web"):      cfs.append(0.65)
                elif v.get("uso_fallback"): cfs.append(0.75)
                else:                       cfs.append(0.82)
            return round(sum(cfs) / len(cfs), 2) if cfs else 0.75
        return round(sum(vals) / len(vals), 2)

    cf_core  = avg_cf(core_files)
    cf_atlas = avg_cf(atlas_files)
    cf_iran  = avg_cf(iran_files)
    cf_global = round((cf_core + cf_atlas + cf_iran) / 3, 2)

    tier1_html = "".join(
        f'<div class="audit-row"><span class="audit-key">{src}</span>'
        f'<span class="audit-val" style="font-family:Share Tech Mono;font-size:0.75em;">CF = {cf:.2f}</span>'
        f'{badge("TIER 1 · No polarizada", "ok")}'
        f'</div>'
        for src, cf in TIER1_CF.items()
    )

    cf_core_bars = (
        cf_tier_bar("SIEG Core",  cf_core,  TIER1_AVG, "#00ff88", "core")  +
        cf_tier_bar("SIEG Atlas", cf_atlas, TIER1_AVG, "#00e5ff", "atlas") +
        cf_tier_bar("SIEG Iran",  cf_iran,  TIER1_AVG, "#ff3333", "iran")  +
        cf_tier_bar("Media SIEG", cf_global,TIER1_AVG, "#ffd700", "global")
    )

    cf_global_color = "#00ff88" if cf_global >= TIER1_AVG - 0.05 else ("#ff8c00" if cf_global >= 0.70 else "#ff3333")

    st.markdown(f"""
    <div class="audit-section" style="border-left:3px solid #ffd700;">
      <div class="audit-title" style="color:#ffd700;">
        ◈ Credibilidad CF — Comparativa vs Fuentes Tier-1 Internacionales
        &nbsp;&nbsp;
        {badge(f"CF Global SIEG: {cf_global:.2f}", "ok" if cf_global >= TIER1_AVG - 0.05 else "warn")}
        &nbsp;
        {badge(f"Referencia Tier-1: {TIER1_AVG:.2f}", "info")}
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;">

        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:var(--muted);
                      letter-spacing:0.12em;margin-bottom:0.8rem;">
            CF SIEG vs MEDIA TIER-1 (barra gris = referencia)
          </div>
          {cf_core_bars}
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.58em;color:var(--muted);
                      margin-top:0.8rem;">
            CF 0.90–1.00 = Tier 1 (BBC/Reuters/NYT) · 0.80–0.89 = Alta fiabilidad ·
            0.70–0.79 = Media · &lt;0.70 = Baja / Google News
          </div>
        </div>

        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.62em;color:var(--muted);
                      letter-spacing:0.12em;margin-bottom:0.8rem;">
            FUENTES TIER-1 DE REFERENCIA (no polarizadas)
          </div>
          {tier1_html}
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.58em;color:var(--muted);
                      margin-top:0.8rem;">
            Criterio Tier-1: internacional · multiperspectiva · verificable · CF ≥ 0.80
          </div>
        </div>

      </div>
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # BLOQUE 4 — RATIO CAPAS (primarias / fallback / web)
    # ════════════════════════════════════════════════════════════

    def count_capas(files_dict):
        n_p = sum(1 for v in files_dict.values() if not v.get("uso_fallback") and not v.get("uso_web"))
        n_f = sum(1 for v in files_dict.values() if v.get("uso_fallback") and not v.get("uso_web"))
        n_w = sum(1 for v in files_dict.values() if v.get("uso_web"))
        return n_p, n_f, n_w

    def capa_bar_html(label, n_p, n_f, n_w, color):
        total = max(n_p + n_f + n_w, 1)
        pp = int(n_p / total * 100)
        fp = int(n_f / total * 100)
        wp = 100 - pp - fp
        health = "ok" if pp >= 60 else ("warn" if pp >= 30 else "err")
        return f"""
        <div style="margin-bottom:1.2rem;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <span style="font-family:'Share Tech Mono',monospace;font-size:0.68em;color:{color};">{label}</span>
            {badge(f"Primarias: {pp}%", health)}
          </div>
          <div style="height:10px;background:rgba(255,255,255,0.04);border-radius:3px;overflow:hidden;display:flex;">
            <div style="width:{pp}%;background:{color};opacity:0.85;" title="Primarias {n_p}"></div>
            <div style="width:{fp}%;background:#ff8c00;opacity:0.7;" title="Fallback {n_f}"></div>
            <div style="width:{wp}%;background:#ff3333;opacity:0.5;" title="Web {n_w}"></div>
          </div>
          <div style="display:flex;gap:1.5rem;margin-top:5px;font-family:'Share Tech Mono',monospace;font-size:0.58em;color:var(--muted);">
            <span style="color:{color};">■ Primarias: {n_p}</span>
            <span style="color:#ff8c00;">■ Fallback: {n_f}</span>
            <span style="color:#ff3333;">■ Google News: {n_w}</span>
          </div>
        </div>"""

    cp_core  = count_capas(core_files)
    cp_atlas = count_capas(atlas_files)
    cp_iran  = count_capas(iran_files)

    total_p = cp_core[0] + cp_atlas[0] + cp_iran[0]
    total_f = cp_core[1] + cp_atlas[1] + cp_iran[1]
    total_w = cp_core[2] + cp_atlas[2] + cp_iran[2]
    total_v = max(total_p + total_f + total_w, 1)
    dep_web = badge(f"{int(total_w/total_v*100)}% Google News", "ok" if total_w/total_v < 0.2 else "warn")

    st.markdown(f"""
    <div class="audit-section" style="border-left:3px solid #ff8c00;">
      <div class="audit-title" style="color:#ff8c00;">
        ◈ Ratio de Capas de Fuentes — Primarias / Fallback / Google News
        &nbsp;&nbsp;
        {dep_web}
      </div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:0.85em;color:#3a5070;margin-bottom:1.2rem;">
        Un sistema saludable obtiene &gt;60% de noticias de fuentes primarias curadas.
        Alta dependencia de Google News (Capa 3) indica falta de fuentes RSS directas para ese actor.
      </div>
      {capa_bar_html("SIEG Core — 14 actores",  *cp_core,  "#00ff88")}
      {capa_bar_html("SIEG Atlas — 6 módulos",  *cp_atlas, "#00e5ff")}
      {capa_bar_html("SIEG Iran — 8 vectores",  *cp_iran,  "#ff3333")}
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # BLOQUE 5 — DETECCIÓN DE SCORES ANÓMALOS / CONGELADOS
    # ════════════════════════════════════════════════════════════

    # Leer histórico para detectar scores congelados
    def load_recent_scores(csv_path, key_col, n_recent=6):
        """Lee últimas N entradas por actor del CSV histórico."""
        result = {}
        try:
            import csv
            rows = []
            with open(csv_path) as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        rows.append(parts)
            rows_sorted = sorted(rows, key=lambda x: float(x[0]) if x[0].replace('.','').isdigit() else 0, reverse=True)
            for ts_s, actor, score_s in rows_sorted:
                try:
                    actor = actor.strip()
                    if actor not in result:
                        result[actor] = []
                    if len(result[actor]) < n_recent:
                        result[actor].append(float(score_s))
                except ValueError:
                    pass
        except Exception:
            pass
        return result

    core_hist  = load_recent_scores(os.path.join(C, "history_log.csv"),       "region")
    atlas_hist = load_recent_scores(os.path.join(A, "history_atlas.csv"),     "modulo")
    iran_hist  = load_recent_scores(os.path.join(I, "history_iran.csv"),      "vector")

    def detect_anomalies(hist_dict, files_dict, system_name, color):
        rows_html = ""
        for key, data in files_dict.items():
            score   = float(data.get("score", data.get("noticias", 0)) if "score" in data else 0)
            # Busca en histórico por key normalizado
            hist_key = next((k for k in hist_dict if k.upper() == key.upper()), None)
            scores_h = hist_dict.get(hist_key, []) if hist_key else []

            # Detectar congelado: últimos N scores iguales
            frozen  = len(scores_h) >= 4 and len(set(round(s) for s in scores_h[:4])) == 1
            # Detectar spike: variación > 20 puntos entre ciclos
            spike   = len(scores_h) >= 2 and abs(scores_h[0] - scores_h[1]) > 20
            # Detectar score 0 o muy bajo sin noticias
            zero    = score < 5

            if frozen:
                status_html = badge("CONGELADO", "warn")
                detail = f"Últimos 4 ciclos: {[round(s) for s in scores_h[:4]]}"
            elif spike:
                status_html = badge(f"SPIKE +{abs(scores_h[0]-scores_h[1]):.0f}pts", "warn")
                detail = f"{scores_h[1]:.0f}% → {scores_h[0]:.0f}%"
            elif zero:
                status_html = badge("SIN DATOS", "err")
                detail = "Score = 0 · posible fallo de fuentes"
            else:
                status_html = badge("NORMAL", "ok")
                detail = f"Score actual: {score:.0f}%"

            rows_html += (
                f'<div class="audit-row">'
                f'<span class="audit-key" style="color:{color};">{key.replace("_"," ")[:20]}</span>'
                f'<span class="audit-val">{detail}</span>'
                f'<span>{status_html}</span>'
                f'</div>'
            )
        return rows_html

    anom_core  = detect_anomalies(core_hist,  core_files,  "Core",  "#00ff88")
    anom_atlas = detect_anomalies(atlas_hist, atlas_files, "Atlas", "#00e5ff")
    anom_iran  = detect_anomalies(iran_hist,  iran_files,  "Iran",  "#ff3333")

    st.markdown(f"""
    <div class="audit-section" style="border-left:3px solid #ff3333;">
      <div class="audit-title" style="color:#ff3333;">
        ◈ Detección de Scores Anómalos o Congelados
      </div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:0.85em;color:#3a5070;margin-bottom:1.2rem;">
        <b style="color:#ff8c00;">CONGELADO</b>: 4+ ciclos con el mismo score exacto — posible fallo de fuente o score mínimo estructural.<br>
        <b style="color:#ff8c00;">SPIKE</b>: variación &gt;20 puntos entre ciclos consecutivos — verificar si es evento real o ruido.<br>
        <b style="color:#ff3333;">SIN DATOS</b>: score = 0 o JSON vacío — fallo de scan o fichero no generado.
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;">
        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.60em;color:#00ff88;
                      letter-spacing:0.15em;margin-bottom:0.6rem;">CORE</div>
          {anom_core}
        </div>
        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.60em;color:#00e5ff;
                      letter-spacing:0.15em;margin-bottom:0.6rem;">ATLAS</div>
          {anom_atlas}
        </div>
        <div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:0.60em;color:#ff3333;
                      letter-spacing:0.15em;margin-bottom:0.6rem;">IRAN</div>
          {anom_iran}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Nota metodológica final ──────────────────────────────────
    st.markdown(f"""
    <div style="background:rgba(0,229,255,0.03);border:1px solid rgba(0,229,255,0.12);
                border-radius:4px;padding:1.2rem 1.8rem;margin-top:0.5rem;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.60em;color:var(--muted);
                  letter-spacing:0.1em;margin-bottom:0.5rem;">◈ NOTA METODOLÓGICA</div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:0.82em;color:#2a4060;line-height:1.8;">
        El CF (Coeficiente de Fiabilidad) es una métrica interna que pondera el peso de cada fuente en el scoring:
        <b style="color:#3a6080;">1.0 = fuente verificada + multiperspectiva</b> · 
        <b style="color:#3a6080;">0.9 = tier-1 internacional (BBC, Reuters, NYT)</b> · 
        <b style="color:#3a6080;">0.8 = alta fiabilidad regional</b> · 
        <b style="color:#3a6080;">0.65 = Google News RSS</b>.<br>
        La comparativa tier-1 indica si el ecosistema SIEG está suficientemente anclado
        en fuentes internacionales no polarizadas. CF global &gt; 0.80 = sistema fiable.
        Los scores SIEG son indicadores de tensión informativa, no predicciones de conflicto.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─── FOOTER ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="hub-footer">
  <div>
    🛡 <strong style="color:var(--text);">SIEG Intelligence Hub V2.2</strong> &nbsp;·&nbsp;
    © {now.year} <strong>M. Castillo</strong> &nbsp;·&nbsp;
    <a href="mailto:mybloggingnotes@gmail.com">mybloggingnotes@gmail.com</a>
  </div>
  <div style="text-align:right;">
    Datos de fuentes abiertas (OSINT) &nbsp;·&nbsp; Solo uso informativo &nbsp;·&nbsp;
    {now_str}
  </div>
</div>
""", unsafe_allow_html=True)
