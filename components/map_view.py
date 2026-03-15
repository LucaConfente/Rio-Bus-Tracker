import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import plotly.graph_objects as go

from data.loader import speed_class, speed_color

MAP_HEIGHT = 920


def render_map_section(df_linha: pd.DataFrame, opts: dict):
    col_map, col_right = st.columns([3, 1.2])

    with col_map:
        _render_map(df_linha, opts)

    with col_right:
        _render_ranking(df_linha)
        _render_donut(df_linha)


# ── Private helpers ──────────────────────────────────────────────────────────

def _render_map(df_linha: pd.DataFrame, opts: dict):
    st.markdown('<div class="section-title">🗺 Mapa de Trajetórias</div>', unsafe_allow_html=True)

    df_map = df_linha.dropna(subset=["latitude", "longitude"]).head(opts["max_pontos"])
    center_lat = df_map["latitude"].mean()
    center_lon = df_map["longitude"].mean()

    tile_map = {
        "CartoDB dark_matter": "CartoDB dark_matter",
        "CartoDB positron":    "CartoDB positron",
        "OpenStreetMap":       "OpenStreetMap",
    }

    m = folium.Map(location=[center_lat, center_lon], zoom_start=13,
                   tiles=tile_map[opts["map_style"]])

    if opts["show_heatmap"]:
        heat_data = [[r["latitude"], r["longitude"]] for _, r in df_map.iterrows()]
        HeatMap(heat_data, radius=10, blur=15, min_opacity=0.3).add_to(m)
    else:
        target = MarkerCluster().add_to(m) if opts["show_clusters"] else m
        for _, row in df_map.iterrows():
            color = speed_color(row["velocidade"])
            popup_html = f"""
            <div style="font-family:monospace;font-size:12px;min-width:160px">
              <b style="font-size:14px">{row['ordem']}</b><br>
              Linha: <b>{row['linha']}</b><br>
              Velocidade: <b>{row['velocidade']} km/h</b><br>
              Status: <b>{speed_class(row['velocidade'])}</b><br>
              Hora: {row['datahora'].strftime('%H:%M:%S')}
            </div>
            """
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5, color=color, fill=True,
                fill_color=color, fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=f"{row['ordem']} · {row['velocidade']} km/h",
            ).add_to(target)

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
         background:#080f1e;border:1px solid #182540;border-radius:12px;
         padding:12px 16px;font-family:monospace;font-size:12px;color:#e2e8f0;">
      <b>🚦 Velocidade</b><br>
      <span style="color:#ef4444">●</span> Parado (0 km/h)<br>
      <span style="color:#f59e0b">●</span> Lento (1-19 km/h)<br>
      <span style="color:#10b981">●</span> Rápido (≥ 20 km/h)
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    st_folium(m, height=MAP_HEIGHT, use_container_width=True)


def _render_ranking(df_linha: pd.DataFrame):
    st.markdown('<div class="section-title">🏆 Ranking de Velocidade</div>', unsafe_allow_html=True)

    top = (
        df_linha.groupby("ordem")["velocidade"].max()
        .reset_index()
        .sort_values("velocidade", ascending=False)
        .head(10)
    )
    max_v = top["velocidade"].max() or 1
    medals = ["🥇", "🥈", "🥉"] + ["🔹"] * 7
    html = ""
    for i, (_, row) in enumerate(top.iterrows()):
        pct = row["velocidade"] / max_v * 100
        html += f"""
        <div class="rank-row">
          <div class="rank-pos">{medals[i]}</div>
          <div class="rank-id">{row['ordem']}</div>
          <div style="flex:1">
            <div class="rank-bar"><div class="rank-bar-fill" style="width:{pct}%"></div></div>
          </div>
          <div class="rank-spd">{row['velocidade']:.0f}<span style="font-size:10px;color:var(--muted)"> km/h</span></div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)


def _render_donut(df_linha: pd.DataFrame):
    st.markdown('<div class="section-title">📊 Distribuição Status</div>', unsafe_allow_html=True)
    total = len(df_linha)
    dist = df_linha["classe"].value_counts().reset_index()
    dist.columns = ["Status", "Qtd"]

    fig = go.Figure(go.Pie(
        labels=dist["Status"], values=dist["Qtd"],
        hole=0.65,
        marker=dict(colors=["#ef4444", "#f59e0b", "#10b981"]),
        textinfo="label+percent",
        textfont=dict(size=11, color="#e2e8f0"),
        showlegend=False,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=220,
        annotations=[dict(text=f"<b>{total}</b><br>registros",
                          x=0.5, y=0.5, showarrow=False,
                          font=dict(color="#e2e8f0", size=13))]
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
