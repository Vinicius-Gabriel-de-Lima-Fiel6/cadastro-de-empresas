import streamlit as st
import auth_db as db

st.set_page_config(page_title="Checkout LabSmartAI", layout="centered")

st.title("🧪 Ative sua Licença LabSmartAI")
st.info("O primeiro cadastro define o Administrador Único da conta.")

with st.form("hotmart_checkout"):
    st.subheader("1. Seus Dados Profissionais")
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome Completo *")
    email = col2.text_input("E-mail de Acesso *")
    cpf_cnpj = col1.text_input("CPF ou CNPJ *")
    whatsapp = col2.text_input("WhatsApp com DDD *")
    
    st.subheader("2. Dados da Empresa")
    empresa = st.text_input("Nome do Laboratório/Empresa *")
    senha = st.text_input("Crie uma senha de acesso *", type="password")

    st.divider()
    st.subheader("3. Pagamento e Plano")
    plano = st.select_slider("Escolha seu plano:", options=["Mensal", "Semestral", "Anual"])
    
    st.write("Bandeiras aceitas:")
    st.markdown("💳 **Visa** | **Mastercard** | **Elo** | 🟢 **PIX**")
    
    metodo = st.radio("Selecione o método:", ["Cartão de Crédito", "PIX", "Boleto"], horizontal=True)

    if metodo == "Cartão de Crédito":
        st.text_input("Número do Cartão", placeholder="0000 0000 0000 0000")
        c1, c2 = st.columns(2)
        c1.text_input("Validade (MM/AA)")
        c2.text_input("CVV")

    st.divider()
    concordo = st.checkbox("Li e aceito os Termos de Uso e Políticas de Privacidade.")
    
    btn = st.form_submit_button("FINALIZAR E ATIVAR MINHA CONTA", use_container_width=True)

if btn:
    if concordo and all([nome, email, cpf_cnpj, empresa, senha]):
        sucesso, msg = db.cadastrar_usuario_completo(
            nome, email, senha, empresa, "ADM", 
            cpf_cnpj, whatsapp, plano, metodo
        )
        if sucesso:
            st.success("✨ Parabéns! Sua empresa foi registrada. Você já pode fazer login.")
            st.balloons()
        else:
            st.error(msg)
    else:
        st.warning("Preencha todos os campos obrigatórios e aceite os termos.")
