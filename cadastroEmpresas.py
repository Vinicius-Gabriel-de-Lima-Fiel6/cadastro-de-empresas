import streamlit as st
import auth_db as db
from email_utils import enviar_email_boas_vindas

def load_css_and_html():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    with open("template.html", "r") as f:
        st.markdown(f.read(), unsafe_allow_html=True)

st.set_page_config(page_title="Checkout LabSmartAI", layout="centered", page_icon="🧪")

# Carrega a "maquiagem" e o esqueleto
load_css_and_html()

with st.form("hotmart_checkout"):
    st.markdown("### 👤 1. Informações de Acesso")
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome Completo *", placeholder="Ex: João Silva")
    email = c2.text_input("E-mail Profissional *", placeholder="contato@empresa.com")
    
    c3, c4 = st.columns(2)
    cpf_cnpj = c3.text_input("CPF ou CNPJ *")
    whatsapp = c4.text_input("WhatsApp (com DDD) *")
    
    st.markdown("---")
    st.markdown("### 🏢 2. Identificação da Empresa")
    empresa = st.text_input("Nome do Laboratório/Empresa *")
    senha = st.text_input("Crie uma Senha Master *", type="password", help="Mínimo 8 caracteres")

    st.markdown("---")
    st.markdown("### 💳 3. Plano e Pagamento")
    
    # Plano em destaque
    plano = st.select_slider("Escolha o período da licença:", options=["Mensal", "Semestral", "Anual"])
    
    # Seletor de método limpo
    metodo = st.radio("Selecione o método de pagamento:", ["Cartão de Crédito", "PIX", "Boleto"], horizontal=True)

    if metodo == "Cartão de Crédito":
        st.markdown("#### Dados do Cartão")
        st.text_input("Número do Cartão", placeholder="0000 0000 0000 0000")
        cc1, cc2 = st.columns(2)
        cc1.text_input("Validade (MM/AA)")
        cc2.text_input("CVV")

    st.markdown("<br>", unsafe_allow_html=True)
    concordo = st.checkbox("Li e aceito os Termos de Uso e Privacidade")
    
    # O Botão agora chama a sua lógica original
    btn = st.form_submit_button("FINALIZAR E ATIVAR MINHA CONTA", use_container_width=True)

    st.markdown("""
        <div class="security-footer">
            🔒 Checkout Protegido com Criptografia SSL 256-bits<br>
            LabSmartAI © 2026 - Todos os direitos reservados.
        </div>
    """, unsafe_allow_html=True)

# LÓGICA DE BACKEND (MANTIDA 100%)
if btn:
    if concordo and all([nome, email, cpf_cnpj, empresa, senha]):
        with st.spinner("Processando pagamento e criando licença..."):
            sucesso, msg = db.cadastrar_usuario_completo(
                nome, email, senha, empresa, "ADM", 
                cpf_cnpj, whatsapp, plano, metodo
            )
            
            if sucesso:
                enviado = enviar_email_boas_vindas(email, nome, empresa)
                st.success("✨ Conta ativada com sucesso!")
                st.balloons()
                if enviado:
                    st.info(f"📧 Credenciais enviadas para **{email}**.")
            else:
                st.error(msg)
    else:
        st.warning("Atenção: Preencha todos os campos obrigatórios e aceite os termos.")
