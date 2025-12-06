import streamlit as st
import pandas as pd
import plotly.express as px

# =================================
# CONFIGURAÇÃO
# =================================
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro – Comparativo 2024 x 2025")

# =================================
# UPLOAD DO ARQUIVO
# =================================
uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Corrigir formatos
    df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce").astype(int)
    df["Faturamento - Valor"] = pd.to_numeric(df["Faturamento - Valor"], errors="coerce")
    df["Meta"] = pd.to_numeric(df["Meta"], errors="coerce")

    # Número do mês para ordenação
    df["Mes_Num"] = df["Mês"].str[:2].astype(int)

    # =================================
    # CARDS DE RESUMO (2024 E 2025)
    # =================================
    st.subheader("📌 Resumo por Ano")

    col1, col2 = st.columns(2)

    for ano, col in zip([2024, 2025], [col1, col2]):

        dados_ano = df[df["Ano"] == ano]

        fat_total = dados_ano["Faturamento - Valor"].sum()
        meta_total = dados_ano["Meta"].sum()
        ating = (fat_total / meta_total * 100) if meta_total > 0 else 0

        col.metric(
            label=f"Ano {ano}",
            value=f"Faturamento: R$ {fat_total:,.0f}".replace(",", "."),
            delta=f"{ating:.1f}% da Meta (Meta: R$ {meta_total:,.0f})".replace(",", ".")
        )

    # =================================
    # GRÁFICO LADO A LADO (DEFINITIVO)
    # =================================
    st.subheader("📊 Comparativo Mensal 2024 x 2025 (Lado a Lado)")

    # AGRUPA para evitar duplicidade → ESSA LINHA É O SEGREDO!
    df_plot = df.groupby(["Mês", "Mes_Num", "Ano"], as_index=False)["Faturamento - Valor"].sum()

    df_plot = df_plot.sort_values(["Mes_Num", "Ano"])

    # Formatação para rótulos
    df_plot["Valor_fmt"] = df_plot["Faturamento - Valor"].apply(
        lambda x: f"R$ {x:,.0f}".replace(",", ".")
    )

    fig = px.bar(
        df_plot,
        x="Mês",
        y="Faturamento - Valor",
        color="Ano",
        barmode="group",       # <--- LADO A LADO REAL
        text="Valor_fmt",
        color_discrete_map={
            2024: "#FF8C00",   # Laranja escuro
            2025: "#005BBB",   # Azul
        }
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="black")
    )

    fig.update_layout(
        yaxis_title="Faturamento (R$)",
        xaxis_title="Mês",
        bargap=0.25,
        height=550,
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =================================
    # TABELA PIVOTADA (FORMATO R$)
    # =================================
    st.subheader("📄 Tabela Comparativa por Ano")

    tabela = df.pivot_table(
        index="Mês",
        columns="Ano",
        values="Faturamento - Valor",
        aggfunc="sum"
    ).reset_index()

    for ano in tabela.columns[1:]:
        tabela[ano] = tabela[ano].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))

    st.dataframe(tabela, use_container_width=True)

else:
    st.info("Envie o arquivo Excel para visualizar o dashboard.")
