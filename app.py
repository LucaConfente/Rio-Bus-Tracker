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