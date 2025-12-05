import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.markdown("""
<style>
    .big-title {
        font-size:36px !important;
        font-weight:700 !important;
        color:#1f4e79 !important;
    }
    .card {
        padding:20px;
        background-color:#f5f5f5;
        border-radius:12px;
        text-align:center;
        margin-bottom:15px;
        font-size:18px;
        font-weight:600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>📊 Dashboard Financeiro – Faturamento & Metas</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    col_mes = [c for c in df.columns if "Mês" in c][0]
    df["Mes_Num"] = df[col_mes].str[:2].astype(int)
    df["Trimestre"] = ((df["Mes_Num"] - 1) // 3) + 1
    df = df.sort_values(["Ano", "Mes_Num"])

    st.sidebar.header("🔍 Filtros")
    anos = sorted(df["Ano"].unique())
    ano_sel = st.sidebar.multiselect("Selecionar Ano", anos, default=anos)
    tri_sel = st.sidebar.multiselect("Selecionar Trimestre", sorted(df["Trimestre"].unique()),
                                     default=sorted(df["Trimestre"].unique()))
    df = df[(df["Ano"].isin(ano_sel)) & (df["Trimestre"].isin(tri_sel))]

    total_fat = df["Faturamento - Valor"].sum()
    total_meta = df["Meta"].sum()
    ating = (total_fat / total_meta * 100) if total_meta > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='card'>💰 Faturamento Total<br>R$ {total_fat:,.2f}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'>🎯 Meta Total<br>R$ {total_meta:,.2f}</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'>📈 Atingimento<br>{ating:.1f}%</div>", unsafe_allow_html=True)

    st.subheader("📊 Faturamento por Ano")
    fig1 = px.line(df, x=col_mes, y="Faturamento - Valor", color="Ano", markers=True, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🎯 Realizado vs Meta")
    fig2 = px.bar(df, x=col_mes, y=["Faturamento - Valor", "Meta"], barmode="group", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 Atingimento da Meta (%)")
    df["Atingimento_%"] = df["Faturamento - Valor"] / df["Meta"] * 100
    fig3 = px.line(df, x=col_mes, y="Atingimento_%", markers=True, template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📋 Dados Filtrados")
    st.dataframe(df)
