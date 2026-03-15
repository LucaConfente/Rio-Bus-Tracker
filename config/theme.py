import streamlit as st


def get_palette(light_mode: bool) -> dict:
    if light_mode:
        return dict(
            bg="#f0f4f8", surface="#ffffff", surface2="#e8edf3", border="#cbd5e1",
            accent="#0284c7", accent2="#059669", green="#059669",
            text="#0f172a", muted="#64748b",
            glow="0 0 20px rgba(2,132,199,.15)",
            glow2="0 0 20px rgba(5,150,105,.15)",
        )
    return dict(
        bg="#040810", surface="#080f1e", surface2="#0d1830", border="#182540",
        accent="#00e5ff", accent2="#10b981", green="#10b981",
        text="#e2e8f0", muted="#64748b",
        glow="0 0 20px rgba(0,229,255,.18)",
        glow2="0 0 20px rgba(16,185,129,.18)",
    )


def inject_css(light_mode: bool):
    p = get_palette(light_mode)

    # ── 1. CSS variables (:root) via f-string ────────────────────────────────
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;500&display=swap');
:root {{
    --bg:        {p['bg']};
    --surface:   {p['surface']};
    --surface2:  {p['surface2']};
    --border:    {p['border']};
    --accent:    {p['accent']};
    --accent2:   {p['accent2']};
    --green:     {p['green']};
    --yellow:    #f59e0b;
    --red:       #ef4444;
    --text:      {p['text']};
    --muted:     {p['muted']};
    --glow:      {p['glow']};
    --glow2:     {p['glow2']};
}}
</style>
""", unsafe_allow_html=True)

    # ── 2. Static component styles ────────────────────────────────────────────
    st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stToolbar"], footer { display: none !important; }

/* ── Sidebar brand ── */
.brand-block {
    display: flex; align-items: center; gap: 12px;
    padding: 18px 0 24px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.brand-icon {
    width: 44px; height: 44px; border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.brand-name { font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: var(--accent); letter-spacing: -0.5px; }
.brand-sub  { font-size: 10px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; }

/* ── KPI cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 20px; }
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color .2s, box-shadow .2s;
}
.kpi-card:hover { border-color: var(--accent); box-shadow: var(--glow); }
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.kpi-label { font-size: 10px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: var(--accent); line-height: 1; }
.kpi-unit  { font-size: 13px; color: var(--muted); margin-left: 4px; }
.kpi-delta { font-size: 12px; color: var(--green); margin-top: 6px; }

/* ── Section titles ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: var(--muted);
    margin: 24px 0 12px;
    display: flex; align-items: center; gap: 8px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── Header banner ── */
.header-banner {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 20px;
    display: flex; align-items: center; justify-content: space-between;
    position: relative; overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--green));
}
.header-line-num {
    font-family: 'Syne', sans-serif;
    font-size: 72px; font-weight: 800;
    color: var(--accent); letter-spacing: -4px; line-height: 1;
}
.header-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(52,211,153,.10);
    border: 1px solid rgba(52,211,153,.28);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px; color: var(--green); font-weight: 600;
    margin-right: 8px;
}
.header-badge.live::before {
    content: ''; width: 6px; height: 6px; border-radius: 50%;
    background: var(--accent);
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: .4; transform: scale(1.4); }
}
.pct-value {
    font-family: 'Syne', sans-serif;
    font-size: 48px; font-weight: 800; color: var(--accent);
}
.header-ghost {
    position: absolute; right: 180px; top: 50%;
    transform: translateY(-50%);
    font-family: 'Syne', sans-serif;
    font-size: 96px; font-weight: 800; opacity: .04;
    pointer-events: none; letter-spacing: -6px;
    color: var(--accent);
}

/* ── Rank table ── */
.rank-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 14px; border-radius: 10px;
    margin-bottom: 6px;
    background: var(--surface2); border: 1px solid var(--border);
    transition: all .15s;
}
.rank-row:hover { border-color: var(--accent); transform: translateX(4px); box-shadow: var(--glow); }
.rank-pos { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--muted); width: 22px; }
.rank-id  { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: var(--text); flex: 1; }
.rank-spd { font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 800; color: var(--accent); }
.rank-bar { flex: 2; height: 4px; background: var(--border); border-radius: 2px; }
.rank-bar-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, var(--accent2), var(--accent)); }

/* ── Pill tags ── */
.pill { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.pill-green  { background: rgba(52,211,153,.15);  color: var(--green); }
.pill-yellow { background: rgba(245,158,11,.15);  color: var(--yellow); }
.pill-red    { background: rgba(239,68,68,.15);   color: var(--red); }
.pill-blue   { background: rgba(0,255,163,.10);   color: var(--accent); }

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)
