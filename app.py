# ================= GRÁFICO LADO A LADO (DEFINITIVO) =================
st.subheader("📊 Comparativo Mensal 2024 x 2025 (Lado a Lado)")

# GARANTE QUE ANO É NUMÉRICO
df["Ano"] = df["Ano"].astype(int)

# AGRUPA — ESSA LINHA ELIMINA O PROBLEMA REAL DO EMPILHAMENTO
df_plot = df.groupby(["Mês", "Mes_Num", "Ano"], as_index=False)["Faturamento - Valor"].sum()

# Ordena
df_plot = df_plot.sort_values(["Mes_Num", "Ano"])

# Formata rótulos
df_plot["Valor_fmt"] = df_plot["Faturamento - Valor"].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))

# Gráfico
fig = px.bar(
    df_plot,
    x="Mês",
    y="Faturamento - Valor",
    color="Ano",
    barmode="group",   # LADO A LADO REAL
    text="Valor_fmt",
    color_discrete_map={
        2024: "#FF8C00",   # Laranja
        2025: "#005BBB",   # Azul
    }
)

fig.update_traces(
    textposition="outside",
    textfont=dict(size=11)
)

fig.update_layout(
    yaxis_title="Faturamento (R$)",
    xaxis_title="Mês",
    bargap=0.25,
    height=550,
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)
