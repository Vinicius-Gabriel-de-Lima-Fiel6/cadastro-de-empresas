import streamlit as st
import auth_db as db
from email_utils import enviar_email_boas_vindas

def aplicar_design_premium():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    with open("template.html", "r") as f:
        st.markdown(f.read(), unsafe_allow_html=True)

st.set_page_config(page_title="Checkout LabSmartAI", layout="centered", page_icon="🧪")

aplicar_design_premium()

with st.form("hotmart_checkout"):
    st.markdown("### 👤 Dados do Administrador")
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome Completo *")
    email = c2.text_input("E-mail de Acesso *")
    
    c3, c4 = st.columns(2)
    cpf_cnpj = c3.text_input("CPF ou CNPJ *")
    whatsapp = c4.text_input("WhatsApp com DDD *")
    
    st.markdown("---")
    st.markdown("### 🏢 Dados da Instituição")
    empresa = st.text_input("Nome do Laboratório/Empresa *")
    senha = st.text_input("Senha de Acesso *", type="password")

    st.markdown("---")
    st.markdown("### 💳 Pagamento e Plano")
    plano = st.select_slider("Escolha o Plano:", options=["Mensal", "Semestral", "Anual"])
    
    metodo = st.radio("Método de Pagamento:", ["Cartão de Crédito", "PIX", "Boleto"], horizontal=True)

    if metodo == "Cartão de Crédito":
        st.text_input("Número do Cartão", placeholder="0000 0000 0000 0000")
        cc1, cc2 = st.columns(2)
        cc1.text_input("Validade (MM/AA)")
        cc2.text_input("CVV")

    st.divider()
    
    # --- TERMOS DE USO DETALHADOS ---
    concordo = st.checkbox("Li e aceito todos os Termos de Uso e Políticas de Privacidade.")
    
    with st.expander("Clique aqui para ler todos os Termos de Uso"):
        st.write("""
            **1. Objeto:** Este contrato regula o acesso à plataforma LabSmartAI.
            **2. Licença:** A licença é pessoal para o administrador e intransmissível.
            **3. Pagamento:** A ativação ocorre após compensação bancária.
            **4. Privacidade:** Os seus dados são protegidos por criptografia e usados apenas para gestão da licença.
            **5. Suporte:** O suporte técnico está disponível em horário comercial.
        """)
    
    btn = st.form_submit_button("FINALIZAR E ATIVAR MINHA CONTA", use_container_width=True)

# LÓGICA DE BACKEND MANTIDA
if btn:
    if concordo and all([nome, email, cpf_cnpj, empresa, senha]):
        with st.spinner("A processar a sua licença..."):
            sucesso, msg = db.cadastrar_usuario_completo(
                nome, email, senha, empresa, "ADM", 
                cpf_cnpj, whatsapp, plano, metodo
            )
            
            if sucesso:
                enviado = enviar_email_boas_vindas(email, nome, empresa)
                st.success("✨ Licença ativada com sucesso!")
                st.balloons()
            else:
                st.error(msg)
    else:
        st.warning("É obrigatório preencher todos os campos e aceitar os termos.")
