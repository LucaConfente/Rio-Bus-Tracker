import streamlit as st
import requests
from datetime import datetime, date, timedelta


@st.cache_data(ttl=300, show_spinner=False)
def _get_linhas() -> list:
    """Busca linhas disponíveis nos últimos 30 minutos para popular o selectbox."""
    agora = datetime.now()
    ini   = (agora - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    fim   = agora.strftime("%Y-%m-%d %H:%M:%S")
    try:
        r = requests.get(
            "https://dados.mobilidade.rio/gps/sppo",
            params={"dataInicial": ini, "dataFinal": fim},
            timeout=15
        )
        data = r.json()
        linhas = sorted(set(item["linha"] for item in data if "linha" in item))
        return ["(Todas)"] + linhas
    except Exception:
        return ["(Todas)"]


def render_sidebar() -> dict | None:
    """Renders the sidebar and returns all filter values as a dict, or error dict if invalid."""
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
            st.caption("📅 Início")
            data_ini = st.date_input(
                "Início",
                value=datetime(2026, 3, 2),
                max_value=date.today(),
                label_visibility="collapsed"
            )
        with col_d2:
            st.caption("📅 Fim")
            data_fim = st.date_input(
                "Fim",
                value=datetime(2026, 3, 2),
                max_value=date.today(),
                label_visibility="collapsed"
            )

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.caption("🕐 Hora início")
            hora_ini = st.time_input("Hora início", value=datetime.strptime("10:00", "%H:%M").time(), label_visibility="collapsed")
        with col_h2:
            st.caption("🕐 Hora fim")
            hora_fim = st.time_input("Hora fim", value=datetime.strptime("10:01", "%H:%M").time(), label_visibility="collapsed")

        dt_ini_str = f"{data_ini} {hora_ini.strftime('%H:%M:%S')}"
        dt_fim_str = f"{data_fim} {hora_fim.strftime('%H:%M:%S')}"

        dt_ini = datetime.strptime(dt_ini_str, "%Y-%m-%d %H:%M:%S")
        dt_fim = datetime.strptime(dt_fim_str, "%Y-%m-%d %H:%M:%S")
        agora  = datetime.now()

        # ── Validações ────────────────────────────────────────────────────────
        erros = []

        if dt_ini > agora:
            erros.append(("🕐", f"Hora inicial <b>{hora_ini.strftime('%H:%M')}</b> está no futuro."))
        if dt_fim > agora:
            erros.append(("🕐", f"Hora final <b>{hora_fim.strftime('%H:%M')}</b> está no futuro."))
        if dt_ini >= dt_fim:
            erros.append(("📅", f"Início <b>{data_ini} {hora_ini.strftime('%H:%M')}</b> deve ser menor que Fim <b>{data_fim} {hora_fim.strftime('%H:%M')}</b>."))
        if dt_fim > dt_ini and (dt_fim - dt_ini) > timedelta(hours=1):
            diff    = dt_fim - dt_ini
            minutos = int(diff.total_seconds() // 60)
            erros.append(("⏱", f"Intervalo de <b>{minutos} min</b> excede o máximo de <b>60 min</b>."))

        if erros:
            erros_html = "".join(
                f'<div class="req-item"><span class="req-icon">{icon}</span><span>{msg}</span></div>'
                for icon, msg in erros
            )
            st.markdown(f"""
            <div class="validation-box">
              <div class="validation-title">⚠️ Filtros inválidos</div>
              <div class="validation-body">{erros_html}</div>
              <div class="validation-footer">
                <div class="req-title">📋 Requisitos</div>
                <div class="req-item"><span class="req-icon">✅</span><span>Hora início &lt; Hora fim</span></div>
                <div class="req-item"><span class="req-icon">✅</span><span>Nenhuma data/hora no futuro</span></div>
                <div class="req-item"><span class="req-icon">✅</span><span>Intervalo máximo de <b>1 hora</b></span></div>
                <div class="req-item"><span class="req-icon">✅</span><span>Intervalo mínimo de <b>1 minuto</b></span></div>
              </div>
            </div>
            <style>
            .validation-box {{
                background: rgba(239,68,68,0.08);
                border: 1px solid rgba(239,68,68,0.35);
                border-radius: 14px;
                padding: 16px;
                margin: 12px 0;
            }}
            .validation-title {{
                font-family: 'Syne', sans-serif;
                font-size: 14px;
                font-weight: 700;
                color: #ef4444;
                margin-bottom: 10px;
                letter-spacing: 1px;
            }}
            .validation-body {{ margin-bottom: 12px; }}
            .req-title {{
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
                text-transform: uppercase;
                color: var(--muted);
                margin-bottom: 8px;
                padding-top: 10px;
                border-top: 1px solid rgba(239,68,68,0.2);
            }}
            .req-item {{
                display: flex;
                align-items: flex-start;
                gap: 8px;
                font-size: 12px;
                color: var(--text);
                margin-bottom: 6px;
                line-height: 1.4;
            }}
            .req-icon {{ font-size: 13px; flex-shrink: 0; }}
            .validation-footer {{ margin-top: 4px; }}
            </style>
            """, unsafe_allow_html=True)
            return {"_erros": erros, "_dt_ini_str": dt_ini_str, "_dt_fim_str": dt_fim_str}

        # ── Filters ───────────────────────────────────────────────────────────
        st.markdown('<div class="section-title">🚌 Filtros</div>', unsafe_allow_html=True)

        with st.spinner("Carregando linhas..."):
            linhas_disp = _get_linhas()

        linha_sel   = st.selectbox("Linha", linhas_disp)
        linha_input = "" if linha_sel == "(Todas)" else linha_sel

        vel_min, vel_max = st.slider("Faixa de velocidade (km/h)", 0, 120, (0, 120))
        if st.button("⟳  Atualizar Dados", width='stretch'):
            st.cache_data.clear()
            st.rerun()

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
