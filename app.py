import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ==========================================
#  CARREGAMENTO DO ARQUIVO
# ==========================================
st.title("📊 Dashboard Financeiro — 2024 x 2025")

file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file)

    # ==========================================
    #  AJUSTES DE COLUNAS
    # ==========================================
    df["Mês"] = df["Mês"].astype(str)
    df["Ano"] = df["Ano"].astype(int)
    df["Faturamento - Valor"] = df["Faturamento - Valor"].astype(float)
    df["Meta"] = df["Meta"].astype(float)

    # ==========================================
    #  RESUMO PARA CARDS
    # ==========================================
    resumo = df.groupby("Ano").agg({
        "Faturamento - Valor": "sum",
        "Meta": "sum"
    }).reset_index()

    resumo["Atingimento"] = resumo["Faturamento - Valor"] / resumo["Meta"]

    col1, col2 = st.columns(2)

    ano_2024 = resumo[resumo["Ano"] == 2024].iloc[0]
    ano_2025 = resumo[resumo["Ano"] == 2025].iloc[0]

    # CARD 2024
    with col1:
        st.markdown(
            f"""
            <div style="padding:20px;border-radius:12px;background:#f4f4f4">
                <h2>📘 Ano 2024</h2>
                <h3>Faturamento: R$ {ano_2024['Faturamento - Valor']:,.0f}</h3>
                <h3>Meta: R$ {ano_2024['Meta']:,.0f}</h3>
                <h3>Atingimento: {ano_2024['Atingimento']*100:.1f}%</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # CARD 2025
    with col2:
        st.markdown(
            f"""
            <div style="padding:20px;border-radius:12px;background:#f4f4f4">
                <h2>📙 Ano 2025</h2>
                <h3>Faturamento: R$ {ano_2025['Faturamento - Valor']:,.0f}</h3>
                <h3>Meta: R$ {ano_2025['Meta']:,.0f}</h3>
                <h3>Atingimento: {ano_2025['Atingimento']*100:.1f}%</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ==========================================
    #  GRÁFICO LADO A LADO (MODELO B)
    # ==========================================
    st.subheader("📊 Comparativo Mensal 2024 x 2025 (Lado a Lado)")

    df_sorted = df.sort_values(["Mês", "Ano"])

    fig = px.bar(
        df_sorted,
        x="Mês",
        y="Faturamento - Valor",
        color="Ano",
        barmode="group",
        text="Faturamento - Valor",
        color_discrete_map={
            2024: "#FF7F0E",   # Laranja escuro
            2025: "#1F77B4"    # Azul
        },
        height=500
    )

    # Labels MAIORES
    fig.update_traces(
        texttemplate="R$ %{y:,.0f}",
        textposition="outside",
        textfont_size=16  # TAMANHO MAIOR
    )

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Faturamento (R$)",
        bargap=0.25,
        legend_title="Ano",
        uniformtext_minsize=16,
        uniformtext_mode="show"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ==========================================
    #  TABELA FINAL FORMATADA
    # ==========================================
    st.subheader("📄 Tabela Consolidada (R$)")

    tabela = df.pivot_table(
        index="Mês",
        columns="Ano",
        values="Faturamento - Valor",
        aggfunc="sum"
    ).fillna(0)

    tabela = tabela.applymap(lambda x: f"R$ {x:,.0f}")

    st.dataframe(tabela, use_container_width=True)

else:
    st.info("Envie a planilha para gerar o dashboard.")

