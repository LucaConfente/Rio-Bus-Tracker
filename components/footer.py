import streamlit as st
import pandas as pd

from data.loader import speed_class


def render_status_cards(df_linha: pd.DataFrame):
    """Three KPI cards: Parados / Lentos / Rápidos."""
    st.markdown('<div class="section-title">🚦 Veículos por Status</div>', unsafe_allow_html=True)

    df_ultimo = df_linha.sort_values("datahora").groupby("ordem").last().reset_index()
    df_ultimo["classe"] = df_ultimo["velocidade"].apply(speed_class)

    n_parado = (df_ultimo["classe"] == "Parado").sum()
    n_lento  = (df_ultimo["classe"] == "Lento").sum()
    n_rapido = (df_ultimo["classe"] == "Rápido").sum()
    total_v  = len(df_ultimo) or 1

    vs1, vs2, vs3 = st.columns(3)

    cards = [
        (vs1, "⛔ Parados",              n_parado, "#ef4444"),
        (vs2, "🐢 Lentos (&lt;20 km/h)", n_lento,  "#f59e0b"),
        (vs3, "🚀 Rápidos (≥20 km/h)",   n_rapido, "#10b981"),
    ]
    for col, label, n, color in cards:
        pct = n / total_v * 100
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-color:{color};border-width:1px;">
              <div class="kpi-label">{label}</div>
              <div><span class="kpi-value" style="color:{color};">{n}</span>
                   <span class="kpi-unit">veículos</span></div>
              <div style="font-size:12px;color:var(--muted);margin-top:6px;">{pct:.1f}% da frota</div>
              <div style="margin-top:14px;height:6px;border-radius:3px;background:var(--border);">
                <div style="width:{pct:.1f}%;height:100%;border-radius:3px;background:{color};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)


def render_footer(df_raw: pd.DataFrame):
    """Stats grid + GitHub button + theme toggle + credits."""
    st.markdown("---")

  
    # ── Stats grid ────────────────────────────────────────────────────────────
    total_reg  = len(df_raw)
    n_veic     = df_raw["ordem"].nunique()
    n_linhas   = df_raw["linha"].nunique()
    vel_media  = df_raw["velocidade"].mean()
    n_parados  = (df_raw["velocidade"] == 0).sum()

    st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:16px;padding:24px 0 8px;">
  <div style="text-align:center;">
    <div style="font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Total Registros</div>
    <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:var(--accent);">{total_reg:,}</div>
  </div>
  <div style="text-align:center;">
    <div style="font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Veículos Únicos</div>
    <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:var(--accent);">{n_veic:,}</div>
  </div>
  <div style="text-align:center;">
    <div style="font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Linhas Ativas</div>
    <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:var(--accent);">{n_linhas:,}</div>
  </div>
  <div style="text-align:center;">
    <div style="font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Vel. Média Geral</div>
    <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:var(--accent);">{vel_media:.1f} <span style="font-size:14px;font-weight:400;color:var(--muted)">km/h</span></div>
  </div>
  <div style="text-align:center;">
    <div style="font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Parados</div>
    <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#ef4444;">{n_parados:,}</div>
  </div>
</div>
<div style="height:1px;background:var(--border);margin:12px 0 16px;"></div>
<p style="text-align:center;color:var(--muted);font-size:11px;margin:0 0 6px;">
  BusTracker · Dados abertos da Mobilidade do Rio de Janeiro ·
  <a href="https://dados.mobilidade.rio" style="color:var(--accent);text-decoration:none;">dados.mobilidade.rio</a>
</p>
<p style="text-align:center;font-size:12px;margin:0 0 12px;letter-spacing:1.5px;font-family:'Syne',sans-serif;">
  <span style="color:var(--muted);">Created by</span>
  <span style="color:var(--accent2);font-weight:700;margin-left:6px;">Luca Confente</span>
</p>
<p style="text-align:center;margin:0 0 24px;">
  <a href="https://github.com/lucaconfente"
     target="_blank"
     style="display:inline-flex;align-items:center;gap:8px;
            background:var(--surface2);border:1px solid var(--border);
            border-radius:10px;padding:8px 20px;
            font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
            color:var(--text);text-decoration:none;
            transition:border-color .2s,box-shadow .2s;"
     onmouseover="this.style.borderColor='var(--accent)';this.style.boxShadow='var(--glow)'"
     onmouseout="this.style.borderColor='var(--border)';this.style.boxShadow='none'">
    ⬡ &nbsp;GitHub
  </a>
</p>
""", unsafe_allow_html=True)
