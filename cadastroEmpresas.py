import streamlit as st
import auth_db as db
from email_utils import enviar_email_boas_vindas

st.set_page_config(page_title="Checkout LabSmartAI", layout="centered", page_icon="🧪")

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
        # Passo 1: Cadastro no Banco
        sucesso, msg = db.cadastrar_usuario_completo(
            nome, email, senha, empresa, "ADM", 
            cpf_cnpj, whatsapp, plano, metodo
        )
        
        if sucesso:
            # Passo 2: Envio de E-mail (Incremento)
            with st.spinner("Processando sua licença e enviando e-mail de acesso..."):
                enviado = enviar_email_boas_vindas(email, nome, empresa)
            
            st.success("✨ Conta ativada com sucesso!")
            st.balloons()
            
            if enviado:
                st.info(f"📧 Enviamos suas credenciais para **{email}**. Verifique sua caixa de entrada.")
            else:
                st.warning("⚠️ Conta criada, mas houve uma falha no envio do e-mail. Acesse o sistema com a senha criada.")
        else:
            st.error(msg)
    else:
        st.warning("Preencha todos os campos obrigatórios e aceite os termos.")
