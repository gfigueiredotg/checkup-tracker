
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Checkup Tracker", layout="wide")
st.title("Checkup Tracker Brazil")

# Listas de opções
produtos = ["Checkup 7000", "Checkup 9000", "Checkup 7000 Luxury", "Checkup 9000 Luxury"]
treinamento_realizado_options = ["Sim", "Não", "Agendado"]
treinamento_vendido_options = ["Sim", "Não"]
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA",
           "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
status_options = ["Entregue", "Backlog"]
facility_options = ["New", "Existent"]

tipo_crm_options = []
bases = ["STARTER", "PROGRAM", "BOOST", "GO HYBRID"]
duracoes = ["12", "24", "36", "48", "60"]
formatos = ["A VISTA", "ANUAL", "MENSAL"]
for base in bases:
    for dur in duracoes:
        for form in formatos:
            tipo_crm_options.append(f"{base} {dur} M {form}")
        tipo_crm_options.append(f"{base} {dur} M SMALL {form}")

# Inicializar session_state
if "checkup_data" not in st.session_state:
    st.session_state["checkup_data"] = []

# Formulário
with st.form("checkup_form"):
    st.subheader("Adicionar Novo Checkup")
    macrolob_options = ["HCP", "HOME", "HR", "CLUB"]
    col1, col2 = st.columns(2)
    cliente = col1.text_input("Nome do Cliente")
    sfid = col2.text_input("SFID")
    macrolob = col1.selectbox("Macrolob", macrolob_options)
    produto = col1.selectbox("Produto", produtos)
    treinamento_vendido = col2.selectbox("Treinamento Vendido?", treinamento_vendido_options)
    treinamento_realizado = col1.selectbox("Treinamento Realizado?", treinamento_realizado_options)
    tipo_crm = col2.selectbox("Tipo de CRM", tipo_crm_options)
    estado = col1.selectbox("Estado", estados)
    vendedor = col2.text_input("Vendedor")
    status = col1.selectbox("Status", status_options)
    data_entrega = col2.date_input("Data de Previsão de Entrega")
    data_fechamento = col1.date_input("Data de Fechamento do Pedido")
    facility = col2.selectbox("Tipo de Facility", facility_options)
    valor = col1.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    observacoes = col2.text_area("Observações")

    submitted = st.form_submit_button("Salvar")
    if submitted:
        st.session_state["checkup_data"].append({
            "Cliente": cliente,
            "SFID": sfid,
            "Macrolob": macrolob,
            "Produto": produto,
            "Treinamento Vendido": treinamento_vendido,
            "Treinamento Realizado": treinamento_realizado,
            "Tipo de CRM": tipo_crm,
            "Estado": estado,
            "Vendedor": vendedor,
            "Status": status,
            "Data de Entrega": str(data_entrega),
            "Data de Fechamento": str(data_fechamento),
            "Facility": facility,
            "Valor": valor,
            "Observações": observacoes
        })
        st.success("Checkup adicionado com sucesso!")

# Dashboard e Tabela
if st.session_state["checkup_data"]:
    df = pd.DataFrame(st.session_state["checkup_data"])

    st.subheader("📊 Dashboard Resumo")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Vendidos", len(df))
    col2.metric("Entregues", len(df[df["Status"] == "Entregue"]))
    col3.metric("Backlog", len(df[df["Status"] == "Backlog"]))

    total_valor = df["Valor"].sum()
    st.metric("💰 Valor Total Vendido", f"R$ {total_valor:,.2f}")
    col4, col5 = st.columns(2)
    col4.metric("Facilities New", len(df[df["Facility"] == "New"]))
    col5.metric("Facilities Existent", len(df[df["Facility"] == "Existent"]))

    st.subheader("Distribuição por Vendedor")
    st.bar_chart(df["Vendedor"].value_counts())

    st.subheader("Distribuição por Estado")
    st.bar_chart(df["Estado"].value_counts())

    macrofiltro = st.selectbox("Filtrar por Macrolob", ["Todos"] + macrolob_options)
    if macrofiltro != "Todos":
        df = df[df["Macrolob"] == macrofiltro]

    st.subheader("📋 Tabela de Checkups")
    st.dataframe(df)
    st.download_button("📥 Exportar CSV", df.to_csv(index=False), "checkup_backlog.csv")
