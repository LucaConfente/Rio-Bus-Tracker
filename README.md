# 🚌 BusTracker — Dashboard de Monitoramento GPS da Mobilidade Urbana do Rio de Janeiro

> Dashboard web interativo para visualização em tempo real do GPS dos ônibus do Rio de Janeiro, construído sobre dados abertos da API pública [dados.mobilidade.rio](https://dados.mobilidade.rio).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://lnkd.in/dBYwAnZ4)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📸 Visão Geral

O BusTracker nasceu de um exercício introdutório em aula no Google Colab explorando a API de GPS do Rio de Janeiro. O projeto foi expandido para um dashboard web completo com mapa interativo, KPIs em tempo real, ranking de veículos, heatmap de densidade e filtros dinâmicos — tudo deployado publicamente via Streamlit Cloud.

---

## ✨ Funcionalidades

### 🗺️ Mapa Interativo
- Visualização simultânea de milhares de veículos GPS sobre o mapa do Rio de Janeiro
- Três estilos de mapa: **CartoDB Dark Matter**, **CartoDB Positron** e **OpenStreetMap**
- **Clustering de marcadores** para performance com grandes volumes de dados
- **Heatmap de densidade** para identificar regiões de maior concentração
- Marcadores coloridos por status de velocidade (🔴 Parado · 🟡 Lento · 🟢 Rápido)
- Popup detalhado por veículo: ID, linha, velocidade, status e horário

### 📊 KPIs em Tempo Real
| Métrica | Descrição |
|---|---|
| ⚡ Velocidade Média | Média de todos os registros filtrados |
| 🏎️ Velocidade Máxima | Pico registrado no intervalo |
| 🚌 Ônibus na Linha | Veículos únicos identificados |
| ⛔ % Parados | Proporção de veículos com velocidade = 0 |

### 🏆 Ranking de Velocidade
- Top 10 veículos com maior velocidade máxima registrada no período
- Barra de progresso visual proporcional ao líder do ranking
- Identificação por medalha (🥇🥈🥉) para os três primeiros

### 🚦 Distribuição por Status
- Gráfico de rosca (donut chart) com distribuição percentual entre Parado / Lento / Rápido
- Cards de status com barra de progresso para cada categoria

### 🔍 Filtros Avançados
- **Período personalizado:** seleção de data + hora início e hora fim
- **Linha de ônibus:** dropdown populado dinamicamente com as linhas disponíveis no período
- **Faixa de velocidade:** slider duplo de 0 a 120 km/h
- **Limite de pontos no mapa:** controle de performance (100 a 5.000 pontos)

### ✅ Validação de Inputs
O sistema valida os filtros em tempo real e bloqueia a execução com feedback visual detalhado quando:
- A hora de início é maior ou igual à hora de fim
- Qualquer data/hora está no futuro
- O intervalo excede o máximo de **1 hora**
- O intervalo é inferior a **1 minuto**

### ⚡ Cache Inteligente
- Requisições à API cacheadas por **5 minutos** via `@st.cache_data`
- Botão "Atualizar Dados" para invalidar o cache manualmente e forçar nova requisição

---

## 🗂️ Estrutura do Projeto

```
BusTracker/
│
├── app.py                   # Entrypoint principal da aplicação
│
├── config/
│   └── theme.py             # Paleta de cores, CSS customizado e injeção de estilos
│
├── data/
│   └── loader.py            # Fetch da API GPS, cache e funções auxiliares de velocidade
│
├── components/
│   ├── sidebar.py           # Sidebar com filtros, validações e opções de mapa
│   ├── header.py            # Banner principal e grid de KPI cards
│   ├── map_view.py          # Mapa Folium, ranking de velocidade e donut chart
│   ├── charts.py            # (reservado para gráficos adicionais)
│   └── footer.py            # Cards de status por categoria e rodapé com estatísticas
│
└── requirements.txt         # Dependências do projeto
```

---

## 🔧 Stack Técnica

| Tecnologia | Uso |
|---|---|
| **Python 3.10+** | Linguagem principal |
| **Streamlit** | Framework web e servidor da aplicação |
| **Folium + streamlit-folium** | Mapa interativo com clustering e heatmap |
| **Plotly** | Gráficos (donut chart de distribuição) |
| **Pandas** | Processamento, filtragem e agregação dos dados |
| **Requests** | Consumo da API REST |
| **API dados.mobilidade.rio** | Fonte de dados GPS em tempo real |
| **Git + GitHub** | Versionamento do código |
| **Streamlit Cloud** | Deploy público gratuito |

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.10 ou superior
- pip

### 1. Clone o repositório
```bash
git clone https://github.com/lucaconfente/bustracker.git
cd bustracker
```

### 2. Crie e ative um ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação
```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`.

---

## 📦 Dependências

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
folium>=0.16.0
streamlit-folium>=0.18.0
plotly>=5.18.0
```

---

## 🌐 API de Dados

Os dados são obtidos em tempo real da API pública do sistema **SPPO** (Sistema de Prioridade ao Transporte Público) do Rio de Janeiro:

```
GET https://dados.mobilidade.rio/gps/sppo
```

**Parâmetros utilizados:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `dataInicial` | string | Data/hora de início (`YYYY-MM-DD HH:MM:SS`) |
| `dataFinal` | string | Data/hora de fim (`YYYY-MM-DD HH:MM:SS`) |
| `linha` | string | Filtro opcional por linha de ônibus |

**Campos retornados utilizados pela aplicação:**

| Campo | Tipo | Descrição |
|---|---|---|
| `ordem` | string | Identificador único do veículo |
| `linha` | string | Código da linha |
| `latitude` | string | Latitude (com vírgula como separador decimal) |
| `longitude` | string | Longitude (com vírgula como separador decimal) |
| `velocidade` | string | Velocidade em km/h |
| `datahora` | string | Timestamp Unix em milissegundos |

> **Nota:** A API retorna latitude e longitude com vírgula como separador decimal. O `loader.py` realiza a conversão automática para float antes do processamento.

---

## 🎨 Sistema de Temas

O projeto suporta dois temas visuais configuráveis via `config/theme.py`:

| | Dark Mode (padrão) | Light Mode |
|---|---|---|
| Background | `#040810` | `#f0f4f8` |
| Surface | `#080f1e` | `#ffffff` |
| Accent | `#00e5ff` | `#0284c7` |
| Accent 2 | `#10b981` | `#059669` |

O CSS é injetado dinamicamente via `st.markdown()` com variáveis CSS (`:root`), garantindo que todos os componentes respondam à troca de tema sem recarregar a página.

---

## 🔄 Fluxo da Aplicação

```
app.py
  │
  ├── render_sidebar()         → retorna filtros validados (ou dict de erros)
  │
  ├── [validação de erros]     → exibe modal de erro e para execução (st.stop)
  │
  ├── fetch_gps()              → requisição à API com cache de 5 min
  │
  ├── [filtragem por velocidade e linha]
  │
  ├── [cálculo de KPIs]
  │
  ├── render_header()          → banner principal + % em movimento
  ├── render_kpi_cards()       → grid com 4 métricas principais
  ├── render_map_section()     → mapa + ranking + donut chart
  ├── render_analysis_charts() → gráficos de análise (charts.py)
  ├── render_data_table()      → tabela de dados brutos
  ├── render_status_cards()    → cards Parado / Lento / Rápido
  └── render_footer()          → estatísticas gerais + créditos
```

---

## 📊 Classificação de Velocidade

| Status | Condição | Cor |
|---|---|---|
| 🔴 Parado | `velocidade == 0` | `#ef4444` |
| 🟡 Lento | `0 < velocidade < 20` | `#f59e0b` |
| 🟢 Rápido | `velocidade >= 20` | `#10b981` |

---

## 🔒 Limites e Restrições

Para garantir performance e evitar sobrecarga na API pública, a aplicação impõe os seguintes limites nos filtros:

- **Intervalo máximo:** 1 hora entre hora início e hora fim
- **Intervalo mínimo:** 1 minuto
- **Datas no futuro:** não permitidas
- **Pontos no mapa:** máximo configurável de 5.000 (padrão: 1.000)

---

## 🚀 Deploy

A aplicação está deployada publicamente via **Streamlit Community Cloud**:

🔗 **[Acessar BusTracker](https://lnkd.in/dBYwAnZ4)**

Para fazer seu próprio deploy:
1. Faça um fork do repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte ao repositório e aponte o arquivo principal como `app.py`
4. Clique em **Deploy**

---

## 👤 Autor

**Luca Confente**

[![GitHub](https://img.shields.io/badge/GitHub-lucaconfente-181717?logo=github)](https://github.com/lucaconfente)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🙏 Agradecimentos

- [Prefeitura do Rio de Janeiro](https://dados.mobilidade.rio) pelos dados abertos de mobilidade urbana
- Comunidade Streamlit pelos recursos e documentação
