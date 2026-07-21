import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MeetMind — AI Meeting Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Theme Tokens ───────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":          "#0D1117",
        "surface":     "#161B22",
        "surface2":    "#21262D",
        "border":      "#30363D",
        "accent":      "#00D4AA",
        "accent2":     "#7C5CFC",
        "text":        "#E6EDF3",
        "text_muted":  "#8B949E",
        "text_dim":    "#484F58",
        "success":     "#3FB950",
        "warning":     "#D29922",
        "error":       "#F85149",
        "card_shadow": "0 4px 24px rgba(0,0,0,0.5)",
        "footer_bg":   "#0A0E13",
    },
    "light": {
        "bg":          "#F0F4F8",
        "surface":     "#FFFFFF",
        "surface2":    "#F6F8FA",
        "border":      "#D0D7DE",
        "accent":      "#00A080",
        "accent2":     "#6448E0",
        "text":        "#1C2128",
        "text_muted":  "#57606A",
        "text_dim":    "#AFB8C1",
        "success":     "#1A7F37",
        "warning":     "#9A6700",
        "error":       "#CF222E",
        "card_shadow": "0 2px 12px rgba(0,0,0,0.08)",
        "footer_bg":   "#1C2128",
    },
}

# ─── Session State ───────────────────────────────────────────────────────────────
for k, v in {
    "theme": "dark", "result": None,
    "chat_history": [], "processing": False, "active_tab": "analyze",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

T = THEMES[st.session_state.theme]

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stApp"] {{
    background-color: {T["bg"]} !important;
    color: {T["text"]} !important;
    font-family: 'Inter', sans-serif;
}}
[data-testid="stSidebar"] {{
    background-color: {T["surface"]} !important;
    border-right: 1px solid {T["border"]} !important;
}}
[data-testid="stSidebar"] > div {{ padding-top: 0 !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton, [data-testid="stToolbar"] {{ display: none; }}
h1,h2,h3,h4 {{ font-family: 'Space Grotesk', sans-serif !important; color: {T["text"]} !important; }}

/* Buttons */
.stButton > button {{
    background: linear-gradient(135deg, {T["accent"]}, {T["accent2"]}) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; font-size: 0.92rem !important;
    padding: 0.55rem 1.3rem !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 14px rgba(0,212,170,0.2) !important;
    letter-spacing: 0.02em !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(0,212,170,0.38) !important;
    filter: brightness(1.07) !important;
}}
.stButton > button:active {{ transform: translateY(0) !important; }}


/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background-color: {T["surface2"]} !important;
    border: 1.5px solid {T["border"]} !important;
    border-radius: 10px !important; color: {T["text"]} !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.92rem !important;
    transition: border-color 0.2s !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {T["accent"]} !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.14) !important;
}}
.stSelectbox > div > div {{
    background-color: {T["surface2"]} !important;
    border: 1.5px solid {T["border"]} !important;
    border-radius: 10px !important; color: {T["text"]} !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {T["bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {T["border"]}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {T["accent"]}; }}

/* ── Components ── */
.meetmind-logo {{
    display: flex; align-items: center; gap: 10px; padding: 20px 16px 12px;
}}
.logo-icon {{
    width: 36px; height: 36px;
    background: linear-gradient(135deg, {T["accent"]}, {T["accent2"]});
    border-radius: 10px; display: flex; align-items: center; justify-content: center;
    font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.1rem;
    color: #fff; flex-shrink: 0;
}}
.logo-name {{
    font-family: 'Space Grotesk', sans-serif; font-weight: 700;
    font-size: 1.15rem; color: {T["text"]}; letter-spacing: -0.02em;
}}
.logo-tag {{
    font-size: 0.65rem; font-weight: 500; color: {T["accent"]};
    letter-spacing: 0.08em; text-transform: uppercase;
}}
.section-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {T["border"]}, transparent);
    margin: 16px 0;
}}

/* Stat card */
.stat-card {{
    background: {T["surface"]}; border: 1px solid {T["border"]};
    border-radius: 14px; padding: 18px 20px;
    box-shadow: {T["card_shadow"]};
    transition: transform 0.2s, box-shadow 0.2s;
}}
.stat-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(0,212,170,0.13);
    border-color: {T["accent"]}55;
}}
.stat-label {{
    font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.1em; color: {T["text_muted"]}; margin-bottom: 6px;
}}
.stat-value {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem; font-weight: 700; line-height: 1;
}}

/* Content card */
.content-card {{
    background: {T["surface"]}; border: 1px solid {T["border"]};
    border-radius: 16px; padding: 24px 28px;
    margin-bottom: 18px; box-shadow: {T["card_shadow"]};
}}
.card-eyebrow {{
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.12em; color: {T["accent"]}; margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
}}
.card-body {{
    font-size: 0.9rem; color: {T["text_muted"]}; line-height: 1.75;
}}

/* Animations */
.pulse-container {{
    display: flex; align-items: center; gap: 6px; padding: 10px 0;
}}
.pulse-dot {{
    width: 8px; height: 8px; border-radius: 50%;
    background: {T["accent"]};
    animation: pulse-wave 1.4s ease-in-out infinite;
}}
.pulse-dot:nth-child(2) {{ animation-delay: 0.2s; }}
.pulse-dot:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes pulse-wave {{
    0%,80%,100% {{ transform: scale(0.7); opacity: 0.4; }}
    40% {{ transform: scale(1.2); opacity: 1; }}
}}
.pulse-label {{
    font-size: 0.86rem; color: {T["text_muted"]};
    font-weight: 500; margin-left: 6px; font-style: italic;
}}

.step-row {{
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid {T["border"]}44;
}}
.step-row:last-child {{ border-bottom: none; }}
.step-icon {{
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700; flex-shrink: 0;
}}
.step-pending {{ background:{T["surface2"]}; border:2px solid {T["border"]}; color:{T["text_dim"]}; }}
.step-running {{
    background:rgba(0,212,170,0.12); border:2px solid {T["accent"]}; color:{T["accent"]};
    animation: spin-ring 1.4s linear infinite;
}}
.step-done {{ background:rgba(63,185,80,0.12); border:2px solid {T["success"]}; color:{T["success"]}; }}
@keyframes spin-ring {{
    0%   {{ box-shadow: 0 -3px 0 0 {T["accent"]}; }}
    25%  {{ box-shadow: 3px 0 0 0 {T["accent"]}; }}
    50%  {{ box-shadow: 0 3px 0 0 {T["accent"]}; }}
    75%  {{ box-shadow: -3px 0 0 0 {T["accent"]}; }}
    100% {{ box-shadow: 0 -3px 0 0 {T["accent"]}; }}
}}
.step-label {{ font-size: 0.88rem; font-weight: 500; color: {T["text"]}; }}

/* Waveform */
.waveform {{
    display: flex; align-items: flex-end; gap: 3px; height: 32px;
}}
.wave-bar {{
    width: 4px; border-radius: 2px;
    background: linear-gradient(180deg, {T["accent"]}, {T["accent2"]});
    animation: wave-bounce 1.2s ease-in-out infinite;
}}
.wave-bar:nth-child(1) {{ height:60%; animation-delay:0.0s; }}
.wave-bar:nth-child(2) {{ height:90%; animation-delay:0.1s; }}
.wave-bar:nth-child(3) {{ height:40%; animation-delay:0.2s; }}
.wave-bar:nth-child(4) {{ height:75%; animation-delay:0.3s; }}
.wave-bar:nth-child(5) {{ height:55%; animation-delay:0.15s; }}
.wave-bar:nth-child(6) {{ height:85%; animation-delay:0.25s; }}
.wave-bar:nth-child(7) {{ height:35%; animation-delay:0.05s; }}
.wave-bar:nth-child(8) {{ height:70%; animation-delay:0.35s; }}
@keyframes wave-bounce {{
    0%,100% {{ transform:scaleY(0.4); opacity:0.5; }}
    50% {{ transform:scaleY(1); opacity:1; }}
}}

/* Hero */
.hero-banner {{
    background: linear-gradient(135deg, {T["surface"]} 0%, {T["surface2"]} 100%);
    border: 1px solid {T["border"]}; border-radius: 20px;
    padding: 36px 40px; margin-bottom: 28px;
    position: relative; overflow: hidden;
}}
.hero-banner::before {{
    content:''; position:absolute; top:-60px; right:-60px;
    width:220px; height:220px;
    background:radial-gradient(circle, {T["accent"]}1A 0%, transparent 70%);
    border-radius:50%;
}}
.hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem; font-weight: 700; color: {T["text"]};
    letter-spacing: -0.03em; line-height: 1.15; margin: 0 0 10px;
}}
.hero-title span {{ color: {T["accent"]}; }}
.hero-sub {{
    font-size: 0.95rem; color: {T["text_muted"]};
    max-width: 500px; line-height: 1.65;
}}

/* Action item rows */
.action-item {{
    display:flex; align-items:flex-start; gap:10px;
    padding:8px 0; border-bottom:1px solid {T["border"]}44;
}}
.action-item:last-child {{ border-bottom:none; }}
.action-dot {{
    width:6px; height:6px; border-radius:50%;
    background:{T["accent"]}; margin-top:6px; flex-shrink:0;
}}
.action-text {{ font-size:0.88rem; color:{T["text_muted"]}; line-height:1.55; }}

/* Chat */
.chat-bubble-user {{
    background: linear-gradient(135deg,{T["accent"]}1A,{T["accent2"]}1A);
    border:1px solid {T["accent"]}44; border-radius:14px 14px 4px 14px;
    padding:12px 16px; font-size:0.9rem; color:{T["text"]};
    margin-left:18%; line-height:1.55;
}}
.chat-bubble-ai {{
    background:{T["surface"]}; border:1px solid {T["border"]};
    border-radius:14px 14px 14px 4px; padding:12px 16px;
    font-size:0.9rem; color:{T["text"]}; margin-right:18%; line-height:1.55;
}}
.chat-role {{
    font-size:0.68rem; font-weight:700; text-transform:uppercase;
    letter-spacing:0.1em; margin-bottom:6px;
}}
.chat-role-user {{ color:{T["accent"]}; }}
.chat-role-ai {{ color:{T["accent2"]}; }}
.typing-indicator {{ display:flex; align-items:center; gap:5px; padding:4px 0; }}
.typing-dot {{
    width:6px; height:6px; background:{T["accent2"]}; border-radius:50%;
    animation: typing 1.0s ease-in-out infinite;
}}
.typing-dot:nth-child(2) {{ animation-delay:0.15s; }}
.typing-dot:nth-child(3) {{ animation-delay:0.3s; }}
@keyframes typing {{
    0%,60%,100% {{ transform:translateY(0); opacity:0.4; }}
    30% {{ transform:translateY(-5px); opacity:1; }}
}}

/* Badges */
.badge {{
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:0.7rem; font-weight:600; letter-spacing:0.06em;
    text-transform:uppercase;
}}
.badge-success {{ background:rgba(63,185,80,0.13); color:{T["success"]}; border:1px solid rgba(63,185,80,0.28); }}
.badge-accent  {{ background:rgba(0,212,170,0.11); color:{T["accent"]};  border:1px solid rgba(0,212,170,0.24); }}
.badge-purple  {{ background:rgba(124,92,252,0.11);color:{T["accent2"]}; border:1px solid rgba(124,92,252,0.24); }}

.transcript-block {{
    background:{T["surface2"]}; border:1px solid {T["border"]};
    border-left:3px solid {T["accent"]}; border-radius:0 10px 10px 0;
    padding:16px 20px; font-family:'JetBrains Mono',monospace;
    font-size:0.78rem; color:{T["text_muted"]}; line-height:1.8;
    max-height:260px; overflow-y:auto; white-space:pre-wrap; word-break:break-word;
}}

/* ── About / scroll sections ── */
.about-section {{
    padding: 64px 0 48px;
    border-top: 1px solid {T["border"]};
}}
.about-section-label {{
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.14em; color: {T["accent"]}; margin-bottom: 12px;
}}
.about-section-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.65rem; font-weight: 700; color: {T["text"]};
    letter-spacing: -0.025em; line-height: 1.2; margin-bottom: 14px;
}}
.about-section-body {{
    font-size: 0.9rem; color: {T["text_muted"]}; line-height: 1.8;
    max-width: 640px;
}}

/* How-it-works steps */
.how-step {{
    display: flex; gap: 18px; align-items: flex-start;
    padding: 20px 0; border-bottom: 1px solid {T["border"]}44;
}}
.how-step:last-child {{ border-bottom: none; }}
.how-step-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem; font-weight: 700;
    color: {T["accent"]}22; line-height: 1;
    min-width: 48px;
}}
.how-step-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem; font-weight: 600; color: {T["text"]}; margin-bottom: 5px;
}}
.how-step-body {{ font-size: 0.86rem; color: {T["text_muted"]}; line-height: 1.65; }}

/* Tech pill */
.tech-grid {{
    display: flex; flex-wrap: wrap; gap: 10px; margin-top: 6px;
}}
.tech-pill {{
    display: inline-flex; align-items: center; gap: 7px;
    background: {T["surface2"]}; border: 1px solid {T["border"]};
    border-radius: 8px; padding: 8px 14px;
    font-size: 0.82rem; font-weight: 500; color: {T["text"]};
    transition: border-color 0.2s, background 0.2s;
}}
.tech-pill:hover {{
    border-color: {T["accent"]}88;
    background: rgba(0,212,170,0.06);
}}
.tech-pill-dot {{
    width: 7px; height: 7px; border-radius: 50%;
}}

/* Orbit animation for tech section icon */
.orbit-ring {{
    width: 90px; height: 90px;
    border: 2px dashed {T["border"]};
    border-radius: 50%;
    position: relative;
    animation: orbit-spin 8s linear infinite;
    flex-shrink: 0;
}}
.orbit-planet {{
    width: 14px; height: 14px;
    border-radius: 50%;
    background: linear-gradient(135deg, {T["accent"]}, {T["accent2"]});
    position: absolute; top: -7px; left: 50%; margin-left: -7px;
}}
@keyframes orbit-spin {{
    from {{ transform: rotate(0deg); }}
    to   {{ transform: rotate(360deg); }}
}}

/* Feature cards grid */
.feature-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px; margin-top: 8px;
}}
.feature-card {{
    background: {T["surface"]}; border: 1px solid {T["border"]};
    border-radius: 14px; padding: 22px 20px;
    transition: transform 0.2s, border-color 0.2s;
}}
.feature-card:hover {{
    transform: translateY(-3px);
    border-color: {T["accent"]}55;
}}
.feature-icon {{
    width: 36px; height: 36px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
    font-weight: 700; color: #fff; margin-bottom: 14px;
}}
.feature-title {{
    font-family: 'Space Grotesk', sans-serif; font-size: 0.92rem;
    font-weight: 600; color: {T["text"]}; margin-bottom: 6px;
}}
.feature-body {{ font-size: 0.8rem; color: {T["text_muted"]}; line-height: 1.6; }}

/* ── Footer ── */
.site-footer {{
    background: {T["footer_bg"]};
    border-top: 1px solid {T["border"]};
    padding: 48px 40px 28px;
    margin-top: 64px;
    border-radius: 20px 20px 0 0;
}}
.footer-brand {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem; font-weight: 700; color: #fff;
    letter-spacing: -0.02em; margin-bottom: 6px;
}}
.footer-tagline {{
    font-size: 0.82rem; color: #6B7280; line-height: 1.6; max-width: 280px;
}}
.footer-col-title {{
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.12em; color: #9CA3AF; margin-bottom: 14px;
}}
.footer-link {{
    display: block; font-size: 0.84rem; color: #6B7280;
    text-decoration: none; margin-bottom: 8px;
    transition: color 0.15s;
}}
.footer-link:hover {{ color: {T["accent"]}; }}
.footer-bottom {{
    border-top: 1px solid #1F2937;
    margin-top: 36px; padding-top: 20px;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 10px;
}}
.footer-copy {{
    font-size: 0.78rem; color: #4B5563;
}}
.footer-made-with {{
    font-size: 0.78rem; color: #4B5563;
}}
.footer-made-with span {{ color: {T["accent"]}; }}


/* 👇 YAHAN PASTE KARO 👇 */
.footer-grid {{
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 32px;
    margin-bottom: 8px;
}}
.footer-logo {{
    display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}}
.footer-divider {{
    height: 1px;
    background: #1F2937;
    margin-top: 12px;
}}
/* 👆 YAHAN TAK 👆 */

/* Blinking cursor */
.blink {{
    display: inline-block; width: 2px; height: 1em;
    background: {T["accent"]}; margin-left: 2px; vertical-align: text-bottom;
    animation: blink-anim 1s step-end infinite;
}}
@keyframes blink-anim {{
    0%,100% {{ opacity:1; }} 50% {{ opacity:0; }}
}}

/* Overrides */
[data-testid="stMarkdownContainer"] p {{ color:{T["text_muted"]}; line-height:1.65; }}
[data-testid="stExpander"] {{
    border:1px solid {T["border"]} !important;
    border-radius:12px !important; background:{T["surface"]} !important;
}}
.streamlit-expanderHeader {{
    font-family:'Space Grotesk',sans-serif !important;
    font-weight:600 !important; color:{T["text"]} !important;
}}
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button *,
.stButton > button,
.stButton > button * {{
    color: #111827 !important;
}}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ─────────────────────────────────────────────────────────────────────
WAVE = ''.join(['<div class="wave-bar"></div>'] * 8)
WAVE_PAUSED = ''.join(['<div class="wave-bar" style="animation-play-state:paused;opacity:0.2;"></div>'] * 8)

def badge(text, kind="accent"):
    return f'<span class="badge badge-{kind}">{text}</span>'

def action_rows(text, dot_color=None):
    items = [l.strip() for l in text.split("\n") if l.strip()]
    style = f'style="background:{dot_color};"' if dot_color else ""
    rows = "".join([
        f'<div class="action-item"><div class="action-dot" {style}></div>'
        f'<div class="action-text">{i}</div></div>'
        for i in items
    ])
    return rows, len(items)

def render_pipeline_steps(states, steps):
    rows = ""
    for i, (label, _) in enumerate(steps):
        s = states[i]
        cls = "step-running" if s == "running" else ("step-done" if s == "done" else "step-pending")
        icon = "✓" if s == "done" else str(i + 1)
        rows += f'<div class="step-row"><div class="step-icon {cls}">{icon}</div><div class="step-label">{label}</div></div>'
    return f"""
    <div class="content-card">
        <div class="card-eyebrow">◈ Pipeline Running</div>
        <div class="pulse-container">
            <div class="pulse-dot"></div><div class="pulse-dot"></div><div class="pulse-dot"></div>
            <span class="pulse-label">Processing your source…</span>
        </div>
        {rows}
    </div>"""


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="meetmind-logo">
        <div class="logo-icon">M</div>
        <div><div class="logo-name">MeetMind</div><div class="logo-tag">AI Intelligence</div></div>
    </div>
    <div class="section-divider"></div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Light", key="light_btn", use_container_width=True):
            st.session_state.theme = "light"; st.rerun()
    with c2:
        if st.button("Dark", key="dark_btn", use_container_width=True):
            st.session_state.theme = "dark"; st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:{T["text_dim"]};padding:0 4px;margin-bottom:8px;">Navigation</div>', unsafe_allow_html=True)

    if st.button("Analyze Source", key="nav_analyze", use_container_width=True):
        st.session_state.active_tab = "analyze"; st.rerun()
    if st.button("Chat with Meeting", key="nav_chat", use_container_width=True):
        st.session_state.active_tab = "chat"; st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:{T["text_dim"]};padding:0 4px;margin-bottom:8px;">Settings</div>', unsafe_allow_html=True)

    language = st.selectbox("Language", ["english", "hinglish", "hindi"], index=0, label_visibility="collapsed")
    st.markdown(f'<div style="font-size:0.74rem;color:{T["text_muted"]};padding:4px 4px 0;">Transcription language</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if st.session_state.result:
        r = st.session_state.result
        wc = len(r.get("transcript", "").split())
        ai_c = len([l for l in r.get("action_items", "").split("\n") if l.strip()])
        st.markdown(f"""
        <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:{T['text_dim']};margin-bottom:10px;">Session Stats</div>
        <div style="display:flex;flex-direction:column;gap:8px;">
            <div style="display:flex;justify-content:space-between;">
                <span style="font-size:0.8rem;color:{T['text_muted']};">Words</span>
                <span style="font-family:'Space Grotesk',sans-serif;font-size:0.85rem;font-weight:600;color:{T['accent']};">{wc:,}</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
                <span style="font-size:0.8rem;color:{T['text_muted']};">Action Items</span>
                <span style="font-family:'Space Grotesk',sans-serif;font-size:0.85rem;font-weight:600;color:{T['accent2']};">{ai_c}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-size:0.8rem;color:{T["text_dim"]};font-style:italic;">No session active</div>', unsafe_allow_html=True)


# ─── ANALYZE TAB ─────────────────────────────────────────────────────────────────
if st.session_state.active_tab == "analyze":

    # Hero
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;">
            <div class="waveform">{WAVE}</div>
            {badge("AI-Powered")}
        </div>
        <div class="hero-title">Turn any meeting into<br><span>structured intelligence</span><div class="blink"></div></div>
        <div class="hero-sub" style="margin-top:12px;">Paste a YouTube URL or a local file path. MeetMind transcribes, summarizes, and extracts every decision and action item — instantly.</div>
    </div>
    """, unsafe_allow_html=True)

    # Input
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-eyebrow">◈ Source Input</div>', unsafe_allow_html=True)
    source_input = st.text_input("source", placeholder="https://youtube.com/watch?v=… or /path/to/recording.mp4", label_visibility="collapsed")
    col_run, col_clear = st.columns([3, 1])
    with col_run:
        run_btn = st.button("Run Analysis", key="run_btn", use_container_width=True)
    with col_clear:
        clear_btn = st.button("Clear", key="clear_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if clear_btn:
        st.session_state.result = None
        st.session_state.chat_history = []
        st.rerun()

    # Pipeline
    if run_btn and source_input.strip():
        steps = [
            ("Downloading & chunking audio",  "process_input"),
            ("Transcribing with Whisper",      "transcribe_all"),
            ("Generating title",               "generate_title"),
            ("Summarizing content",            "summarize"),
            ("Extracting action items",        "extract_action_items"),
            ("Extracting key decisions",       "extract_key_decisions"),
            ("Identifying open questions",     "extract_questions"),
            ("Building RAG index",             "build_rag_chain"),
        ]
        ph = st.empty()
        try:
            from utils.audio_processor import process_input
            from core.transcriber import transcribe_all
            from core.summarize import summarize, generate_title
            from core.extractor import extract_action_items, extract_key_decisions, extract_questions
            from core.rag_engine import build_rag_chain

            states = ["pending"] * len(steps)
            fns = [
                lambda: process_input(source_input.strip()),
                lambda chunks=None: transcribe_all(chunks, language),
                lambda t=None: generate_title(t),
                lambda t=None: summarize(t),
                lambda t=None: extract_action_items(t),
                lambda t=None: extract_key_decisions(t),
                lambda t=None: extract_questions(t),
                lambda t=None: build_rag_chain(t),
            ]

            states[0] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            chunks = process_input(source_input.strip()); states[0] = "done"

            states[1] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            transcript = transcribe_all(chunks, language); states[1] = "done"

            states[2] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            title = generate_title(transcript); states[2] = "done"

            states[3] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            summary = summarize(transcript); states[3] = "done"

            states[4] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            action_items = extract_action_items(transcript); states[4] = "done"

            states[5] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            decisions = extract_key_decisions(transcript); states[5] = "done"

            states[6] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            questions = extract_questions(transcript); states[6] = "done"

            states[7] = "running"; ph.markdown(render_pipeline_steps(states, steps), unsafe_allow_html=True)
            rag_chain = build_rag_chain(transcript); states[7] = "done"

            ph.empty()
            st.session_state.result = dict(
                title=title, transcript=transcript, summary=summary,
                action_items=action_items, key_decisions=decisions,
                open_questions=questions, rag_chain=rag_chain,
            )
            st.session_state.chat_history = []
            st.rerun()

        except ImportError as e:
            ph.empty(); st.error(f"Import error: {e}")
        except Exception as e:
            ph.empty(); st.error(f"Pipeline error: {e}")

    elif run_btn:
        st.warning("Please enter a YouTube URL or file path.")

    # Results
    if st.session_state.result:
        r = st.session_state.result
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin:8px 0 22px;">
            {badge("Analysis Complete","success")}
            <span style="font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:600;color:{T['text']};">{r.get('title','Untitled')}</span>
        </div>
        """, unsafe_allow_html=True)

        wc = len(r.get("transcript", "").split())
        ai_c = len([l for l in r.get("action_items", "").split("\n") if l.strip()])
        dec_c = len([l for l in r.get("key_decisions", "").split("\n") if l.strip()])
        q_c = len([l for l in r.get("open_questions", "").split("\n") if l.strip()])

        for col, lbl, val, col_hex in zip(
            st.columns(4),
            ["Word Count", "Action Items", "Decisions", "Open Questions"],
            [f"{wc:,}", str(ai_c), str(dec_c), str(q_c)],
            [T["accent"], T["accent2"], T["success"], T["warning"]],
        ):
            with col:
                st.markdown(f'<div class="stat-card"><div class="stat-label">{lbl}</div><div class="stat-value" style="color:{col_hex};">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="content-card"><div class="card-eyebrow">◈ Summary</div><div class="card-body">{r.get("summary","").replace(chr(10),"<br>")}</div></div>', unsafe_allow_html=True)

        col_a, col_d = st.columns(2)
        with col_a:
            rows, cnt = action_rows(r.get("action_items", ""))
            none_html_a = f'<span style="color:{T["text_dim"]}">None detected</span>'
            st.markdown(f'<div class="content-card"><div class="card-eyebrow">◈ Action Items</div>{badge(str(cnt) + " tasks")}<br><br>{rows or none_html_a}</div>', unsafe_allow_html=True)
        with col_d:
            rows_d, cnt_d = action_rows(r.get("key_decisions", ""), T["accent2"])
            accent2 = T["accent2"]
            text_dim = T["text_dim"]
            none_html_d = f'<span style="color:{text_dim}">None detected</span>'
            st.markdown(f'<div class="content-card"><div class="card-eyebrow" style="color:{accent2};">◈ Key Decisions</div>{badge(str(cnt_d) + " decisions", "purple")}<br><br>{rows_d or none_html_d}</div>', unsafe_allow_html=True)

        q_items_txt = r.get("open_questions", "")
        if q_items_txt.strip():
            rows_q, _ = action_rows(q_items_txt, T["warning"])
            st.markdown(f'<div class="content-card"><div class="card-eyebrow" style="color:{T["warning"]};">◈ Open Questions</div>{rows_q}</div>', unsafe_allow_html=True)

        with st.expander("Raw Transcript", expanded=False):
            st.markdown(f'<div class="transcript-block">{r.get("transcript","")}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:8px;padding:18px 22px;background:linear-gradient(135deg,{T["accent"]}0D,{T["accent2"]}0D);border:1px solid {T["accent"]}33;border-radius:14px;">
            <div style="font-family:'Space Grotesk',sans-serif;font-weight:600;color:{T['text']};margin-bottom:4px;">Ready to chat with this meeting?</div>
            <div style="font-size:0.83rem;color:{T['text_muted']};">Ask anything — decisions, context, follow-ups — powered by RAG.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Chat Interface", key="goto_chat"):
            st.session_state.active_tab = "chat"; st.rerun()


# ─── CHAT TAB ────────────────────────────────────────────────────────────────────
elif st.session_state.active_tab == "chat":

    if not st.session_state.result:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;padding:80px 0;text-align:center;">
            <div class="waveform" style="margin-bottom:20px;">{WAVE_PAUSED}</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;font-weight:600;color:{T['text']};margin-bottom:8px;">No meeting loaded yet</div>
            <div style="font-size:0.88rem;color:{T['text_muted']};">Run an analysis first, then come back to chat.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Analyze", key="back_to_analyze"):
            st.session_state.active_tab = "analyze"; st.rerun()
    else:
        r = st.session_state.result
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:22px;">
            <div class="waveform">{WAVE}</div>
            <div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;color:{T['text']};">Chat with your meeting</div>
                <div style="font-size:0.77rem;color:{T['text_muted']};">{r.get('title','Untitled')} &nbsp;·&nbsp; RAG-powered Q&amp;A</div>
            </div>
            <div style="margin-left:auto;">{badge("Active","success")}</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown(f'<div style="text-align:center;padding:40px 0 20px;color:{T["text_dim"]};font-size:0.88rem;font-style:italic;">Ask anything about your meeting — decisions, tasks, who said what…</div>', unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div style="margin-bottom:14px;"><div class="chat-role chat-role-user">You</div><div class="chat-bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="margin-bottom:14px;"><div class="chat-role chat-role-ai">MeetMind</div><div class="chat-bubble-ai">{msg["content"]}</div></div>', unsafe_allow_html=True)

        question = st.chat_input("Ask about your meeting…", key="chat_input")
        if question:
            try:
                from core.rag_engine import ask_question
                st.session_state.chat_history.append({"role": "user", "content": question})
                ph2 = st.empty()
                ph2.markdown(f'<div class="chat-bubble-ai" style="margin-right:20%;"><div class="chat-role chat-role-ai">MeetMind</div><div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div></div>', unsafe_allow_html=True)
                answer = ask_question(r["rag_chain"], question)
                ph2.empty()
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        if st.session_state.chat_history:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Clear Conversation", key="clear_chat"):
                st.session_state.chat_history = []; st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# ─── SCROLLABLE ABOUT / HOW-IT-WORKS / TECH SECTIONS ──────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

# ── What is MeetMind ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="about-section">
    <div class="about-section-label">About the Project</div>
    <div class="about-section-title">What is MeetMind?</div>
    <div class="about-section-body">
        MeetMind is an end-to-end AI pipeline that converts any audio — a YouTube recording, a Zoom call, a local MP4 —
        into a structured knowledge artifact. You get a clean transcript, an AI-written summary, extracted action items,
        key decisions, and open questions, all in under a minute. Then you can ask follow-up questions in plain language
        and get grounded answers backed by the actual meeting content.
    </div>
    <br>
    <div class="about-section-body">
        Built as a B.Tech project exploring how modern LLM pipelines can make institutional knowledge instantly
        accessible — no more scrubbing through hour-long recordings or hunting through dense meeting notes.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Features grid ─────────────────────────────────────────────────────────────
feat_accent = T["accent"]
feat_purple = T["accent2"]
feat_green  = T["success"]
feat_warn   = T["warning"]

st.markdown(f"""
<div style="padding-bottom: 48px; border-top: 1px solid {T['border']}; padding-top: 48px;">
    <div class="about-section-label">Core Capabilities</div>
    <div class="about-section-title">Everything a meeting produces,<br>automatically extracted</div>
    <div class="feature-grid" style="margin-top:28px;">
        <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,{feat_accent},{feat_purple});">TR</div>
            <div class="feature-title">Auto Transcription</div>
            <div class="feature-body">Whisper-powered speech-to-text that handles accented English, Hinglish, and background noise. Works on YouTube links and local files alike.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,{feat_purple},{feat_warn});">AI</div>
            <div class="feature-title">LLM Summarization</div>
            <div class="feature-body">A compact, coherent summary generated by a large language model — not keyword extraction. Captures intent, not just words.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,{feat_green},{feat_accent});">EX</div>
            <div class="feature-title">Structured Extraction</div>
            <div class="feature-body">Action items, key decisions, and open questions — each surfaced as a clean list, ready to paste into Notion, Jira, or your email.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,{feat_warn},{feat_purple});">RAG</div>
            <div class="feature-title">RAG-powered Chat</div>
            <div class="feature-body">Ask natural-language questions about your meeting. The retrieval-augmented system finds the right context before the LLM answers — no hallucination.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-section">
    <div class="about-section-label">PIPELINE WALKTHROUGH</div>
    <div class="about-section-title">How It Works</div>
</div>
""", unsafe_allow_html=True)

steps = [
    (
        "01",
        "Audio Acquisition & Preprocessing",
        "The application accepts either a YouTube URL or a local file. "
        "For YouTube, yt-dlp extracts the audio. Pydub then splits it into overlapping 60-second chunks."
    ),
    (
        "02",
        "Speech-to-Text",
        "Each chunk is transcribed using Whisper. The transcripts are merged while removing overlap."
    ),
    (
        "03",
        "LLM Analysis",
        "The transcript is processed by GPT-4o/Groq/Ollama to generate the title, summary, action items, decisions and questions."
    ),
    (
        "04",
        "RAG Index",
        "Sentence embeddings are generated and stored in FAISS. LangChain manages retrieval."
    ),
    (
        "05",
        "Interactive Q&A",
        "Relevant transcript chunks are retrieved and provided to the LLM so answers stay grounded."
    )
]

for num, title, body in steps:
    st.markdown(f"""
    <div class="how-step">
        <div class="how-step-num">{num}</div>
        <div>
            <div class="how-step-title">{title}</div>
            <div class="how-step-body">{body}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Tech Stack ────────────────────────────────────────────────────────────────
tech_stacks = [
    ("#00D4AA", "Python 3.11",         "Core language"),
    ("#7C5CFC", "OpenAI Whisper",       "Speech-to-text"),
    ("#D29922", "LangChain",            "LLM orchestration"),
    ("#3FB950", "FAISS",                "Vector search"),
    ("#F85149", "yt-dlp",               "YouTube download"),
    ("#00D4AA", "pydub",                "Audio processing"),
    ("#7C5CFC", "Sentence Transformers","Embeddings"),
    ("#D29922", "GPT-4o / Groq",        "Language model"),
    ("#3FB950", "Streamlit",            "UI framework"),
    ("#00D4AA", "python-dotenv",        "Config management"),
]

_t_text = T["text"]
_t_muted = T["text_muted"]
pills_html = "".join([
    '<div class="tech-pill"><div class="tech-pill-dot" style="background:' + c + ';"></div><div><div style="font-weight:600;font-size:0.82rem;color:' + _t_text + ';">' + name + '</div><div style="font-size:0.72rem;color:' + _t_muted + ';">' + role + '</div></div></div>'
    for c, name, role in tech_stacks
])

st.markdown(f"""
<div style="padding: 48px 0; border-top: 1px solid {T['border']};">
    <div style="display:flex;align-items:center;gap:28px;flex-wrap:wrap;">
        <div>
            <div class="about-section-label">Tech Stack</div>
            <div class="about-section-title">Built with</div>
            <div class="about-section-body" style="margin-bottom:24px;">
                Every layer of the stack is open-source or freely accessible via API, making this
                deployable on a laptop or a free-tier cloud instance.
            </div>
            <div class="tech-grid">{pills_html}</div>
        </div>
        <div style="flex-shrink:0;margin-left:auto;">
            <div class="orbit-ring"><div class="orbit-planet"></div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ─── FOOTER ───────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
footer_html = f"""
<div class="site-footer">
    <div class="footer-grid">
        <div>
            <div class="footer-logo">
                <div class="logo-icon">M</div>
                <div class="footer-brand">MeetMind</div>
            </div>
            <p class="footer-tagline">AI-powered meeting intelligence that converts meeting recordings into searchable insights, summaries, action items and interactive Q&amp;A.</p>
        </div>
        <div>
            <div class="footer-col-title">Project</div>
            <a class="footer-link" href="#">Overview</a>
            <a class="footer-link" href="#">Architecture</a>
            <a class="footer-link" href="#">Documentation</a>
            <a class="footer-link" href="#">Release Notes</a>
        </div>
        <div>
            <div class="footer-col-title">Technology</div>
            <a class="footer-link" href="https://openai.com/research/whisper" target="_blank">Whisper</a>
            <a class="footer-link" href="https://python.langchain.com/" target="_blank">LangChain</a>
            <a class="footer-link" href="https://faiss.ai/" target="_blank">FAISS</a>
            <a class="footer-link" href="https://streamlit.io/" target="_blank">Streamlit</a>
        </div>
        <div>
            <div class="footer-col-title">Resources</div>
            <a class="footer-link" href="#">GitHub</a>
            <a class="footer-link" href="#">Project Report</a>
            <a class="footer-link" href="#">Demo Video</a>
            <a class="footer-link" href="#">Contact</a>
        </div>
    </div>
    <div class="footer-divider"></div>
    <div class="footer-bottom">
        <span class="footer-copy">&copy; 2025 MeetMind &bull; 2026 Project</span>
        <span class="footer-made-with">Built with Python &bull; Streamlit &bull; Whisper &bull; LangChain &bull; FAISS &bull; GPT-4o</span>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)