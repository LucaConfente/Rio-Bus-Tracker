import sys
import os

# ── Fix sys.path para Windows + Streamlit ─────────────────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
_cwd  = os.getcwd()
for _p in [_here, _cwd]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

# ── Page config (deve ser a primeira chamada Streamlit) ───────────────────────
st.set_page_config(
    page_title="BusTracker · GPS Mobilidade Urbana",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme state (antes da injeção de CSS) ─────────────────────────────────────
if "light_mode" not in st.session_state:
    st.session_state.light_mode = False

# ── Imports dos módulos ───────────────────────────────────────────────────────
from config.theme        import inject_css
from data.loader         import fetch_gps, speed_class
from components.sidebar  import render_sidebar
from components.header   import render_header, render_kpi_cards
from components.map_view import render_map_section
from components.charts   import render_analysis_charts, render_data_table
from components.footer   import render_status_cards, render_footer

# ── CSS ───────────────────────────────────────────────────────────────────────
inject_css(st.session_state.light_mode)

# ── Sidebar → retorna todos os filtros ───────────────────────────────────────
opts = render_sidebar()

# ── Exibe erro central se filtros inválidos ───────────────────────────────────
if opts and "_erros" in opts:
    erros_html = "".join(
        f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;font-size:14px;color:#e2e8f0">'
        f'<span style="font-size:18px;flex-shrink:0">{icon}</span><span>{msg}</span></div>'
        for icon, msg in opts["_erros"]
    )
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:center;min-height:60vh;">
      <div style="background:#080f1e;border:1px solid rgba(239,68,68,0.4);border-radius:24px;
                  padding:40px 48px;max-width:520px;width:100%;text-align:left;
                  box-shadow:0 0 40px rgba(239,68,68,0.1);">
        <div style="font-size:48px;margin-bottom:16px;text-align:center">🚫</div>
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                    color:#ef4444;margin-bottom:6px;text-align:center;letter-spacing:-0.5px;">
          Filtros Inválidos
        </div>
        <div style="font-size:12px;color:#64748b;text-align:center;
                    letter-spacing:2px;text-transform:uppercase;margin-bottom:28px;">
          Corrija os erros na barra lateral
        </div>
        <div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.2);
                    border-radius:14px;padding:20px;margin-bottom:20px;">
          {erros_html}
        </div>
        <div style="border-top:1px solid #182540;padding-top:16px;">
          <div style="font-size:10px;color:#64748b;letter-spacing:2px;
                      text-transform:uppercase;margin-bottom:12px;">📋 Requisitos</div>
          <div style="font-size:13px;color:#94a3b8;line-height:2">
            ✅ &nbsp;Hora início &lt; Hora fim<br>
            ✅ &nbsp;Nenhuma data/hora no futuro<br>
            ✅ &nbsp;Intervalo máximo de <b style="color:#e2e8f0">1 hora</b><br>
            ✅ &nbsp;Intervalo mínimo de <b style="color:#e2e8f0">1 minuto</b>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Carrega e filtra dados ────────────────────────────────────────────────────
with st.spinner("Carregando dados GPS..."):
    df_raw = fetch_gps(opts["dt_ini_str"], opts["dt_fim_str"], opts["linha_input"])

if df_raw.empty:
    st.warning("Nenhum dado retornado para os filtros selecionados.")
    st.stop()

df = df_raw[
    (df_raw["velocidade"] >= opts["vel_min"]) &
    (df_raw["velocidade"] <= opts["vel_max"])
].copy()
df["classe"] = df["velocidade"].apply(speed_class)

linha_sel = opts["linha_input"]
if linha_sel and linha_sel in df["linha"].values:
    df_linha     = df[df["linha"] == linha_sel]
    titulo_linha = linha_sel
else:
    df_linha     = df
    titulo_linha = "TODAS"

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_registros = len(df_linha)
vel_media       = df_linha["velocidade"].mean()
vel_max         = df_linha["velocidade"].max()
n_veiculos      = df_linha["ordem"].nunique()
n_linhas        = df_linha["linha"].nunique()
pct_movimento   = (df_linha["velocidade"] > 0).mean() * 100
pct_parado      = 100 - pct_movimento
n_parados_raw   = (df_linha["velocidade"] == 0).sum()

# ── Renderiza a página ────────────────────────────────────────────────────────
render_header(titulo_linha, opts["dt_ini_str"], pct_movimento, n_veiculos, total_registros)
render_kpi_cards(vel_media, vel_max, n_veiculos, n_linhas, pct_parado, n_parados_raw)
render_map_section(df_linha, opts)
render_analysis_charts(df, df_linha, vel_media)
render_data_table(df_linha)
render_status_cards(df_linha)
render_footer(df_raw)