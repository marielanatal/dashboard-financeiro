import streamlit as st
import pandas as pd
import plotly.express as px

# ================= CONFIGURAÇÃO =================
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro – Comparativo 2024 x 2025")

# ================= UPLOAD =================
uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Normaliza dados numéricos
    df["Faturamento - Valor"] = pd.to_numeric(df["Faturamento - Valor"], errors="coerce")
    df["Meta"] = pd.to_numeric(df["Meta"], errors="coerce")

    # GARANTE QUE ANO É INTEIRO → EVITA GRÁFICO EMPILHADO
    df["Ano"] = df["Ano"].astype(int)

    # Extrai número do mês para ordenar
    df["Mes_Num"] = df["Mês"].str[:2].astype(int)

    # ================= CARDS RESUMIDOS =================
    st.subheader("📌 Indicadores Gerais")

    col1, col2 = st.columns(2)

    for ano, col in zip([2024, 2025], [col1, col2]):
        df_ano = df[df["Ano"] == ano]

        fat_total = df_ano["Faturamento - Valor"].sum()
        meta_total = df_ano["Meta"].sum()
        ating = (fat_total / meta_total) * 100 if meta_total > 0 else 0

        col.metric(
            label=f"Resumo {ano}",
            value=f"Faturamento: R$ {fat_total:,.0f}".replace(",", "."),
            delta=f"{ating:.1f}% da Meta (Meta: R$ {meta_total:,.0f})".replace(",", ".")
        )

    # ================= GRÁFICO LADO A LADO =================
    st.subheader("📊 Comparativo Mensal 2024 x 2025 (Lado a Lado)")

    df_plot = df[df["Ano"].isin([2024, 2025])].copy()
    df_plot = df_plot.sort_values(["Mes_Num", "Ano"])

    df_plot["Valor_fmt"] = df_plot["Faturamento - Valor"].apply(
        lambda x: f"R$ {x:,.0f}".replace(",", ".")
    )

    fig = px.bar(
        df_plot,
        x="Mês",
        y="Faturamento - Valor",
        color="Ano",
        barmode="group",  # LADO A LADO REAL
        text="Valor_fmt",
        color_discrete_map={
            2024: "#FF8C00",  # Laranja escuro
            2025: "#005BBB",  # Azul forte
        }
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="black")
    )

    fig.update_layout(
        yaxis_title="Faturamento (R$)",
        xaxis_title="Mês",
        bargap=0.25,
        height=550,
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ================= TABELA FINAL PIVOTADA =================
    st.subheader("📄 Tabela Comparativa (Pivotada)")

    tabela = df.pivot_table(
        index="Mês",
        columns="Ano",
        values="Faturamento - Valor",
        aggfunc="sum"
    ).reset_index()

    for ano in [2024, 2025]:
        if ano in tabela.columns:
            tabela[ano] = tabela[ano].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))

    st.dataframe(tabela, use_container_width=True)

else:
    st.info("Envie o arquivo Excel para visualizar o dashboard.")



