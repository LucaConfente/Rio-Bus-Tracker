import streamlit as st
from datetime import datetime


def render_sidebar() -> dict:
    """Renders the sidebar and returns all filter values as a dict."""
    with st.sidebar:
        st.markdown("""
        <div class="brand-block">
          <div class="brand-icon">🚌</div>
          <div>
            <div class="brand-name">BusTracker</div>
            <div class="brand-sub">GPS · Mobilidade Urbana</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Period ────────────────────────────────────────────────────────────
        st.markdown('<div class="section-title">⏱ Período</div>', unsafe_allow_html=True)
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            data_ini = st.date_input("Início", value=datetime(2026, 3, 2), label_visibility="collapsed")
        with col_d2:
            data_fim = st.date_input("Fim",    value=datetime(2026, 3, 2), label_visibility="collapsed")

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            hora_ini = st.time_input("Hora início", value=datetime.strptime("10:00", "%H:%M").time(), label_visibility="collapsed")
        with col_h2:
            hora_fim = st.time_input("Hora fim",    value=datetime.strptime("10:01", "%H:%M").time(), label_visibility="collapsed")

        dt_ini_str = f"{data_ini} {hora_ini}:00"
        dt_fim_str = f"{data_fim} {hora_fim}:00"

        # ── Filters ───────────────────────────────────────────────────────────
        st.markdown('<div class="section-title">🚌 Filtros</div>', unsafe_allow_html=True)
        linha_input = st.text_input("Linha (deixe vazio para todas)", placeholder="Ex: 630")
        vel_min, vel_max = st.slider("Faixa de velocidade (km/h)", 0, 120, (0, 120))
        st.button("⟳  Atualizar Dados", width='stretch')

        # ── Map options ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">🗺 Visualização do Mapa</div>', unsafe_allow_html=True)
        map_style     = st.selectbox("Estilo", ["CartoDB dark_matter", "CartoDB positron", "OpenStreetMap"], label_visibility="collapsed")
        show_heatmap  = st.checkbox("Heatmap de densidade", value=False)
        show_clusters = st.checkbox("Agrupar marcadores",   value=True)
        max_pontos    = st.slider("Máx. pontos no mapa", 100, 5000, 1000, 100)

        st.markdown("---")
        st.caption("Dados: [dados.mobilidade.rio](https://dados.mobilidade.rio)")

    return dict(
        dt_ini_str=dt_ini_str,
        dt_fim_str=dt_fim_str,
        linha_input=linha_input.strip(),
        vel_min=vel_min,
        vel_max=vel_max,
        map_style=map_style,
        show_heatmap=show_heatmap,
        show_clusters=show_clusters,
        max_pontos=max_pontos,
    )
