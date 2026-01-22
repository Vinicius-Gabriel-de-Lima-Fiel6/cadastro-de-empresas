import streamlit as st
import auth_db as db
from email_utils import enviar_email_boas_vindas


def aplicar_identidade_visual():
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        with open("template.html", "r", encoding="utf-8") as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivos de design (CSS/HTML) não encontrados.")

st.set_page_config(page_title="Checkout LabSmartAI", layout="centered", page_icon="🧪")


aplicar_identidade_visual()


with st.form("hotmart_checkout"):
    st.markdown("### 👤 Informações do Administrador")
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome Completo *", placeholder="Digite seu nome")
    email = col2.text_input("E-mail de Acesso *", placeholder="email@exemplo.com")
    
    col3, col4 = st.columns(2)
    cpf_cnpj = col3.text_input("CPF ou CNPJ *")
    whatsapp = col4.text_input("WhatsApp com DDD *")
    
    st.markdown("---")
    st.markdown("### 🏢 Dados da Instituição")
    empresa = st.text_input("Nome do Laboratório/Empresa *")
    senha = st.text_input("Crie uma Senha Master *", type="password")

    st.markdown("---")
    st.markdown("### 💳 Plano e Pagamento")
    plano = st.select_slider("Selecione o Plano:", options=["Mensal", "Semestral", "Anual"])
    
    metodo = st.radio("Forma de Pagamento:", ["Cartão de Crédito", "PIX", "Boleto"], horizontal=True)

    if metodo == "Cartão de Crédito":
        st.text_input("Número do Cartão", placeholder="0000 0000 0000 0000")
        cc1, cc2 = st.columns(2)
        cc1.text_input("Validade (MM/AA)")
        cc2.text_input("CVV")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Checkbox de termos
    concordo = st.checkbox("Li e aceito todos os Termos de Uso e Políticas de Privacidade.")
    
    # Expander com o texto dos termos
    with st.expander("Visualizar Termos de Uso"):
        st.write("""
            Ao ativar sua conta, você concorda com a licença de uso do software LabSmartAI, 
            o processamento de dados para fins cadastrais e o envio de comunicações de suporte.
        """)
    
    # Botão que dispara sua lógica original
    btn = st.form_submit_button("FINALIZAR E ATIVAR MINHA CONTA", use_container_width=True)


if btn:
    if concordo and all([nome, email, cpf_cnpj, empresa, senha]):
        with st.spinner("Processando sua ativação no sistema..."):
            # Chama sua função de banco original
            sucesso, msg = db.cadastrar_usuario_completo(
                nome, email, senha, empresa, "ADM", 
                cpf_cnpj, whatsapp, plano, metodo
            )
            
            if sucesso:
             
                enviado = enviar_email_boas_vindas(email, nome, empresa)
                
                st.success("✨ Licença LabSmartAI ativada com sucesso!")
                st.balloons()
                
                if enviado:
                    st.info(f"📧 Enviamos os detalhes de acesso para **{email}**.")
            else:
                st.error(msg)
    else:
        st.warning("Preencha todos os campos obrigatórios e aceite os termos.")
