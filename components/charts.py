import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


GRID_COLOR  = "#1e2e4a"
FONT_COLOR  = "#e2e8f0"
CHART_BG    = "rgba(0,0,0,0)"


def _layout(height=320, **extra):
    return dict(
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        font=dict(color=FONT_COLOR, size=11), title_font_size=13,
        margin=dict(t=40, b=10, l=10, r=10), height=height,
        **extra,
    )


def render_analysis_charts(df: pd.DataFrame, df_linha: pd.DataFrame, vel_media: float):
    st.markdown('<div class="section-title">📈 Análise Detalhada</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        top_linhas = (
            df.groupby("linha").size()
            .reset_index(name="registros")
            .sort_values("registros", ascending=False)
            .head(15)
        )
        fig = px.bar(
            top_linhas, x="registros", y="linha", orientation="h",
            title="Top Linhas por Registros",
            color="registros",
            color_continuous_scale=["#152038", "#10b981"],
        )
        fig.update_layout(**_layout(
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed", gridcolor=GRID_COLOR),
            xaxis=dict(gridcolor=GRID_COLOR),
        ))
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    with c2:
        fig2 = px.histogram(
            df_linha, x="velocidade", nbins=30,
            title="Distribuição de Velocidades",
            color_discrete_sequence=["#10b981"],
        )
        fig2.add_vline(x=vel_media, line_dash="dash", line_color="#10b981",
                       annotation_text=f"Média {vel_media:.1f}",
                       annotation_font_color="#10b981")
        fig2.update_layout(**_layout(
            xaxis=dict(gridcolor=GRID_COLOR, title="km/h"),
            yaxis=dict(gridcolor=GRID_COLOR, title="Veículos"),
            showlegend=False,
        ))
        st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

    with c3:
        top10 = df.groupby("linha")["velocidade"].mean().nlargest(10).index
        df_box = df[df["linha"].isin(top10)]
        fig3 = px.box(
            df_box, x="linha", y="velocidade",
            title="Velocidade por Linha (Top 10)",
            color_discrete_sequence=["#10b981"],
        )
        fig3.update_layout(**_layout(
            xaxis=dict(gridcolor=GRID_COLOR, title="Linha"),
            yaxis=dict(gridcolor=GRID_COLOR, title="km/h"),
            showlegend=False,
        ))
        st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})


def render_data_table(df_linha: pd.DataFrame):
    st.markdown('<div class="section-title">📋 Tabela de Registros GPS</div>', unsafe_allow_html=True)

    col_search, col_limit = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Filtrar por ordem ou linha",
                               placeholder="Ex: B31075 ou 630",
                               label_visibility="collapsed")
    with col_limit:
        limite = st.selectbox("Linhas", [50, 100, 250, 500], label_visibility="collapsed")

    df_table = df_linha.copy()
    if search:
        df_table = df_table[
            df_table["ordem"].str.contains(search, case=False, na=False) |
            df_table["linha"].str.contains(search, case=False, na=False)
        ]

    df_show = df_table[["ordem", "linha", "velocidade", "latitude",
                         "longitude", "datahora", "classe"]].head(limite).copy()
    df_show["velocidade"] = df_show["velocidade"].apply(lambda v: f"{v:.0f} km/h")
    df_show["latitude"]   = df_show["latitude"].round(5)
    df_show["longitude"]  = df_show["longitude"].round(5)
    df_show["datahora"]   = df_show["datahora"].dt.strftime("%H:%M:%S")
    df_show.columns       = ["Ordem", "Linha", "Velocidade", "Latitude",
                              "Longitude", "Hora", "Status"]

    st.dataframe(
        df_show,
        width='stretch',
        height=360,
        column_config={
            "Velocidade": st.column_config.TextColumn("Velocidade"),
            "Status":     st.column_config.TextColumn("Status"),
        }
    )
