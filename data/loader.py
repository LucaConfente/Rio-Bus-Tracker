import streamlit as st
import pandas as pd
import requests


# Depois — cache por 5 minutos mas respeita os parâmetros
@st.cache_data(ttl=300, show_spinner=False)
def fetch_gps(data_inicial: str, data_final: str, linha: str = "") -> pd.DataFrame:
    url = "https://dados.mobilidade.rio/gps/sppo"
    params = {"dataInicial": data_inicial, "dataFinal": data_final}
    if linha:
        params["linha"] = linha
    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()
        df = pd.DataFrame(data)
        df["latitude"]   = df["latitude"].str.replace(",", ".").astype(float)
        df["longitude"]  = df["longitude"].str.replace(",", ".").astype(float)
        df["velocidade"] = pd.to_numeric(df["velocidade"], errors="coerce").fillna(0)
        df["datahora"]   = pd.to_datetime(df["datahora"].astype(float), unit="ms")
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()


def speed_class(v: float) -> str:
    if v == 0:   return "Parado"
    elif v < 20: return "Lento"
    else:        return "Rápido"


def speed_color(v: float) -> str:
    if v == 0:   return "#ef4444"
    elif v < 20: return "#f59e0b"
    else:        return "#10b981"


def speed_pill(v: float) -> str:
    cls_map = {"Parado": "pill-red", "Lento": "pill-yellow", "Rápido": "pill-green"}
    c = speed_class(v)
    return f'<span class="pill {cls_map[c]}">{c}</span>'
