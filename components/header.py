import streamlit as st


def render_header(titulo_linha: str, dt_ini_str: str, pct_movimento: float,
                  n_veiculos: int, total_registros: int):
    st.markdown(f"""
<div class="header-banner">
  <div>
    <div style="font-size:10px;color:var(--muted);letter-spacing:3px;text-transform:uppercase;margin-bottom:4px;">Linha Selecionada</div>
    <div class="header-line-num">{titulo_linha}</div>
    <div style="margin-top:10px;">
      <span class="header-badge live">Tempo Real</span>
      <span class="header-badge" style="background:rgba(0,229,255,.08);border-color:rgba(0,229,255,.25);color:var(--accent);">📍 Rio de Janeiro, RJ</span>
      <span class="header-badge" style="background:rgba(16,185,129,.08);border-color:rgba(16,185,129,.25);color:var(--accent2);">{dt_ini_str[:16]}</span>
    </div>
  </div>
  <div class="header-ghost">BUS</div>
  <div style="text-align:right">
    <div style="font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Em Movimento</div>
    <div class="pct-value">{pct_movimento:.1f}%</div>
    <div style="font-size:12px;color:var(--muted);margin-top:4px;">{n_veiculos} veículos · {total_registros:,} registros GPS</div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_kpi_cards(vel_media: float, vel_max: float, n_veiculos: int,
                     n_linhas: int, pct_parado: float, n_parados_raw: int):
    st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">⚡ Velocidade Média</div>
    <div><span class="kpi-value">{vel_media:.1f}</span><span class="kpi-unit">km/h</span></div>
    <div class="kpi-delta">↑ Fluxo ativo</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">🏎 Velocidade Máxima</div>
    <div><span class="kpi-value">{vel_max:.0f}</span><span class="kpi-unit">km/h</span></div>
    <div class="kpi-delta" style="color:var(--yellow);">Pico registrado</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">🚌 Ônibus na Linha</div>
    <div><span class="kpi-value">{n_veiculos}</span><span class="kpi-unit">veículos</span></div>
    <div class="kpi-delta">{n_linhas} linhas ativas</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">⛔ Parados</div>
    <div><span class="kpi-value" style="color:var(--red);">{pct_parado:.1f}</span><span class="kpi-unit">%</span></div>
    <div class="kpi-delta" style="color:var(--muted);">{n_parados_raw} veículos parados</div>
  </div>
</div>
""", unsafe_allow_html=True)
