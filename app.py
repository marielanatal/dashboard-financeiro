import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Financeiro",
    layout="wide"
)

st.title("📊 Dashboard Financeiro")

# ==============================
# Upload do arquivo
# ==============================
st.subheader("Envie sua planilha Excel")
uploaded_file = st.file_uploader("Selecione o arquivo", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Garantir formatação numérica
    df["Faturamento - Valor"] = pd.to_numeric(df["Faturamento - Valor"], errors="coerce")
    df["Meta"] = pd.to_numeric(df["Meta"], errors="coerce")

    # Extrai número do mês para ordenar
    df["Mês_num"] = df["Mês"].str[:2].astype(int)

    # ==============================
    # CARDS POR ANO
    # ==============================
    st.subheader("📌 Indicadores Gerais")

    col1, col2 = st.columns(2)

    for ano, col in zip([2024, 2025], [col1, col2]):
        df_ano = df[df["Ano"] == ano]

        fat_total = df_ano["Faturamento - Valor"].sum()
        meta_total = df_ano["Meta"].sum()

        ating = (fat_total / meta_total) * 100 if meta_total > 0 else 0

        col.metric(
            label=f"Faturamento Total {ano}",
            value=f"R$ {fat_total:,.0f}".replace(",", "."),
            delta=f"Atingimento da Meta: {ating:.1f}%"
        )

    # ==============================
    # GRÁFICO COMPARATIVO LADO A LADO
    # ==============================
    st.subheader("📊 Comparativo Mensal 2024 x 2025 (Lado a Lado)")

    df_comp = df[df["Ano"].isin([2024, 2025])].copy()
    df_comp = df_comp.sort_values(["Mês_num", "Ano"])

    # Criar coluna formatada para texto nas barras
    df_comp["Valor_fmt"] = df_comp["Faturamento - Valor"].apply(
        lambda x: f"R$ {x:,.0f}".replace(",", ".")
    )

    fig_comp = px.bar(
        df_comp,
        x="Mês",
        y="Faturamento - Valor",
        color="Ano",
        barmode="group",  # LADO A LADO
        text="Valor_fmt",
        color_discrete_map={
            2024: "#FF8C00",  # Laranja escuro
            2025: "#0047AB"   # Azul forte
        },
        labels={
            "Faturamento - Valor": "Faturamento (R$)",
            "Mês": "Mês"
        }
    )

    fig_comp.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="black")
    )

    fig_comp.update_layout(
        yaxis_title="Faturamento (R$)",
        xaxis_title="Mês",
        bargap=0.25,
        plot_bgcolor="white",
        title_font=dict(size=22)
    )

    st.plotly_chart(fig_comp, use_container_width=True)

    # ==============================
    # TABELA FINAL (FORMATADA)
    # ==============================
    st.subheader("📄 Dados Consolidados")

    df_display = df.copy()
    df_display["Faturamento - Valor"] = df_display["Faturamento - Valor"].apply(
        lambda x: f"R$ {x:,.0f}".replace(",", ".")
    )
    df_display["Meta"] = df_display["Meta"].apply(
        lambda x: f"R$ {x:,.0f}".replace(",", ".")
    )

    st.dataframe(df_display, use_container_width=True)

else:
    st.info("Envie um arquivo Excel para iniciar.")

