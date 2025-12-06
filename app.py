import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- CONFIGURAÇÃO DO APP --------------------
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.markdown("""
<style>
    .big-title {
        font-size:36px !important;
        font-weight:700 !important;
        color:#1f4e79 !important;
        margin-bottom:20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>📊 Dashboard Financeiro – Faturamento & Metas</div>", unsafe_allow_html=True)

# -------------------- UPLOAD --------------------
uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Identifica automaticamente a coluna "Mês"
    col_mes = [c for c in df.columns if "Mês" in c][0]

    # Preparação dos dados
    df["Mes_Num"] = df[col_mes].str[:2].astype(int)
    df["Trimestre"] = ((df["Mes_Num"] - 1) // 3) + 1

    df = df.sort_values(["Ano", "Mes_Num"])

    # -------------------- FILTROS --------------------
    st.sidebar.header("🔍 Filtros")

    anos = sorted(df["Ano"].unique())
    ano_sel = st.sidebar.multiselect("Selecionar Ano", anos, default=anos)

    tri_sel = st.sidebar.multiselect(
        "Selecionar Trimestre",
        sorted(df["Trimestre"].unique()),
        default=sorted(df["Trimestre"].unique())
    )

    df = df[(df["Ano"].isin(ano_sel)) & (df["Trimestre"].isin(tri_sel))]

    # -------------------- KPIs ESTILO DIRETORIA --------------------

    # Cálculos principais
    fat_total = df["Faturamento - Valor"].sum()
    meta_total = df["Meta"].sum()
    ating_total = (fat_total / meta_total * 100) if meta_total > 0 else 0

    # Crescimento Ano/Ano
    fat_por_ano = df.groupby("Ano")["Faturamento - Valor"].sum().sort_index()
    if len(fat_por_ano) >= 2:
        ano_atual = fat_por_ano.index[-1]
        ano_anterior = fat_por_ano.index[-2]
        crescimento_ano = (
            (fat_por_ano.loc[ano_atual] - fat_por_ano.loc[ano_anterior])
            / fat_por_ano.loc[ano_anterior] * 100
        )
    else:
        crescimento_ano = 0

    # Diferença absoluta vs Meta
    diferenca_meta = fat_total - meta_total

    # Função de card premium
    def kpi_card(titulo, valor, sufixo="", icone="📌", cor="black"):
        return f"""
        <div style="
            background-color:white;
            padding:22px;
            border-radius:14px;
            box-shadow:0px 2px 8px rgba(0,0,0,0.15);
            text-align:center;
            border-left:6px solid {cor};
        ">
            <div style="font-size:24px; font-weight:700;">{icone} {titulo}</div>
            <div style="font-size:32px; font-weight:800; margin-top:10px;">
                {valor}{sufixo}
            </div>
        </div>
        """

    # Cores condicionais
    cor_ating = "#2ecc71" if ating_total >= 100 else "#e74c3c"
    cor_cres = "#2ecc71" if crescimento_ano >= 0 else "#e74c3c"
    cor_dif = "#2ecc71" if diferenca_meta >= 0 else "#e74c3c"

    # Linha de KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(kpi_card("Faturamento Total", f"R$ {fat_total:,.2f}", "", "💰", "#3498db"), unsafe_allow_html=True)

    with col2:
        st.markdown(kpi_card("Atingimento da Meta", f"{ating_total:.1f}", "%", "🎯", cor_ating), unsafe_allow_html=True)

    with col3:
        st.markdown(kpi_card("Crescimento Ano/Ano", f"{crescimento_ano:.1f}", "%", "📈", cor_cres), unsafe_allow_html=True)

    with col4:
        st.markdown(kpi_card("Diferença vs Meta", f"R$ {diferenca_meta:,.2f}", "", "📊", cor_dif), unsafe_allow_html=True)

    # -------------------- GRÁFICO 1 --------------------
    st.subheader("📊 Faturamento por Ano")
    fig1 = px.line(df, x=col_mes, y="Faturamento - Valor", color="Ano", markers=True, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

    # -------------------- GRÁFICO 2 --------------------
    st.subheader("🎯 Realizado vs Meta")
    fig2 = px.bar(df, x=col_mes, y=["Faturamento - Valor", "Meta"], barmode="group", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

    # -------------------- GRÁFICO 3 --------------------
    st.subheader("📈 Atingimento da Meta (%)")
    df["Atingimento_%"] = df["Faturamento - Valor"] / df["Meta"] * 100
    fig3 = px.line(df, x=col_mes, y="Atingimento_%", markers=True, template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

    # -------------------- TABELA --------------------
    st.subheader("📋 Dados Filtrados")
    st.dataframe(df)
