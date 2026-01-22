import streamlit as st
import auth_db as db
from email_utils import enviar_email_boas_vindas

def aplicar_design():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    with open("template.html", "r") as f:
        st.markdown(f.read(), unsafe_allow_html=True)

st.set_page_config(page_title="Checkout LabSmartAI", layout="centered", page_icon="🧪")

# Aplica o visual "Perfeito e Limpo"
aplicar_design()

# Mantendo toda a sua lógica original...
with st.form("hotmart_checkout"):
    st.subheader("1. Dados do Administrador")
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome Completo *")
    email = col2.text_input("E-mail de Acesso *")
    cpf_cnpj = col1.text_input("CPF ou CNPJ *")
    whatsapp = col2.text_input("WhatsApp *")
    
    st.subheader("2. Sobre o Laboratório")
    empresa = st.text_input("Nome da Instituição/Empresa *")
    senha = st.text_input("Crie uma Senha Master *", type="password")

    st.divider()
    st.subheader("3. Configuração do Plano")
    plano = st.select_slider("Assinatura:", options=["Mensal", "Semestral", "Anual"])
    
    metodo = st.radio("Forma de Pagamento:", ["Cartão de Crédito", "PIX", "Boleto"], horizontal=True)

    if metodo == "Cartão de Crédito":
        st.text_input("Número do Cartão", placeholder="0000 0000 0000 0000")
        c1, c2 = st.columns(2)
        c1.text_input("Validade")
        c2.text_input("CVV")

    st.divider()
    concordo = st.checkbox("Declaro que li e aceito os Termos de Uso.")
    
    # O botão agora terá o estilo gradiente mentolado do CSS
    btn = st.form_submit_button("FINALIZAR E ATIVAR AGORA", use_container_width=True)

# Lógica de Backend (Processamento real)
if btn:
    if concordo and all([nome, email, cpf_cnpj, empresa, senha]):
        with st.spinner("Validando sua licença..."):
            sucesso, msg = db.cadastrar_usuario_completo(
                nome, email, senha, empresa, "ADM", 
                cpf_cnpj, whatsapp, plano, metodo
            )
            
            if sucesso:
                enviar_email_boas_vindas(email, nome, empresa)
                st.success("✨ Conta ativada com sucesso!")
                st.balloons()
            else:
                st.error(msg)
    else:
        st.warning("Preencha os campos obrigatórios e aceite os termos.")
