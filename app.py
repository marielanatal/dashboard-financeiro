import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- CONFIGURAÇÃO --------------------
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.markdown("""
<style>
.big-title {
    font-size: 36px !important;
    font-weight: 700 !important;
    color: #1f4e79 !important;
}
.kpi-box {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.15);
}
.kpi-title {
    font-size: 20px;
    font-weight: 600;
    color: #444;
}
.kpi-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>📊 Dashboard Financeiro – Comparativo 2024 x 2025</div>", unsafe_allow_html=True)

# -------------------- UPLOAD --------------------
uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Identifica nome da coluna de Mês
    col_mes = [c for c in df.columns if "Mês" in c][0]

    # Criar número do mês
    df["Mes_Num"] = df[col_mes].str[:2].astype(int)

    df = df.sort_values(["Ano", "Mes_Num"])

    anos = sorted(df["Ano"].unique())
    dados_anos = {}

    for ano in anos:
        df_ano = df[df["Ano"] == ano]
        fat = df_ano["Faturamento - Valor"].sum()
        meta = df_ano["Meta"].sum()
        ating = (fat / meta * 100) if meta > 0 else 0

        dados_anos[ano] = {"fat": fat, "meta": meta, "ating": ating}

    # -------------------- KPIs --------------------
    st.subheader("📌 Indicadores por Ano")

    colunas = st.columns(len(anos))

    for i, ano in enumerate(anos):
        with colunas[i]:
            st.markdown("<div class='kpi-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-title'>Ano {ano}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>Faturamento<br>R$ {dados_anos[ano]['fat']:,.0f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>Meta<br>R$ {dados_anos[ano]['meta']:,.0f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>Atingimento<br>{dados_anos[ano]['ating']:.1f}%</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # -------------------- GRÁFICO --------------------
    st.subheader("📊 Comparativo Mensal 2024 x 2025 (Lado a Lado)")

    fig = px.bar(
        df,
        x=col_mes,
        y="Faturamento - Valor",
        color="Ano",
        barmode="group",
        text=df["Faturamento - Valor"].apply(lambda x: f"R$ {x:,.0f}"),
        template="plotly_white",
        color_discrete_map={
            anos[0]: "#F28E2B",  # laranja
            anos[1]: "#1F77B4"   # azul
        }
    )

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Faturamento (R$)",
        legend_title="Ano",
        bargap=0.12,
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------- TABELA --------------------
    st.subheader("📋 Dados Detalhados")

    df_show = df.copy()
    df_show["Faturamento - Valor"] = df_show["Faturamento - Valor"].apply(lambda x: f"R$ {x:,.2f}")
    df_show["Meta"] = df_show["Meta"].apply(lambda x: f"R$ {x:,.2f}")

    st.dataframe(df_show, use_container_width=True)
