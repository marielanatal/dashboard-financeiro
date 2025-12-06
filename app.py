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
.kpi-card {
    background-color: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.15);
}
.kpi-title {
    font-size: 20px;
    font-weight: 700;
}
.kpi-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>📊 Dashboard Financeiro – Comparativo 2024 x 2025</div>", unsafe_allow_html=True)

# -------------------- UPLOAD --------------------
uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Identificando coluna de mês automaticamente
    col_mes = [c for c in df.columns if "Mês" in c][0]

    df["Mes_Num"] = df[col_mes].str[:2].astype(int)
    df = df.sort_values(["Ano", "Mes_Num"])

    # -------------------- CALCULOS POR ANO --------------------
    anos = sorted(df["Ano"].unique())
    
    dados_anos = {}

    for ano in anos:
        df_ano = df[df["Ano"] == ano]

        fat = df_ano["Faturamento - Valor"].sum()
        meta = df_ano["Meta"].sum()
        ating = (fat / meta * 100) if meta > 0 else 0

        dados_anos[ano] = {
            "fat": fat,
            "meta": meta,
            "ating": ating
        }

    # -------------------- KPIs POR ANO --------------------
    st.subheader("📌 Indicadores por Ano")

    cols = st.columns(len(anos))

    for i, ano in enumerate(anos):
        with cols[i]:
            st.markdown(f"<div class='kpi-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-title'>📅 Ano {ano}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>Faturamento:<br> R$ {dados_anos[ano]['fat']:,.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>Meta:<br> R$ {dados_anos[ano]['meta']:,.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>Atingimento:<br> {dados_anos[ano]['ating']:.1f}%</div>", unsafe_allow_html=True)
            st.markdown(f"</div>", unsafe_allow_html=True)

    # -------------------- GRÁFICO COMPARATIVO --------------------
    st.subheader("📊 Comparativo Mensal 2024 x 2025")

    fig = px.bar(
        df,
        x=col_mes,
        y="Faturamento - Valor",
        color="Ano",
        barmode="group",
        text_auto=".2s",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Faturamento (R$)",
        legend_title="Ano",
        bargap=0.15
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------- TABELA COM R$ --------------------
    st.subheader("📋 Dados Detalhados")

    df_display = df.copy()
    df_display["Faturamento - Valor"] = df_display["Faturamento - Valor"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Meta"] = df_display["Meta"].apply(lambda x: f"R$ {x:,.2f}")

    st.dataframe(df_display, use_container_width=True)
