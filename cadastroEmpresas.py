import streamlit as st
import auth_db as db

st.set_page_config(page_title="Onboarding LabSmartAI", page_icon="🧪", layout="centered")

# CSS para estilizar os cartões e seleção
st.markdown("""
    <style>
    .plan-card {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Checkout LabSmartAI PRO")
st.write("Complete seu cadastro para ativar sua licença empresarial.")

with st.form("checkout_form"):
    # --- SEÇÃO 1: IDENTIDADE DO ADM ---
    st.subheader("1. Dados do Responsável")
    col1, col2 = st.columns(2)
    with col1:
        nome_adm = st.text_input("Nome Completo")
        email = st.text_input("E-mail de Acesso")
    with col2:
        cpf_cnpj = st.text_input("CPF ou CNPJ")
        whatsapp = st.text_input("WhatsApp com DDD")
    
    senha = st.text_input("Crie uma senha de acesso", type="password")

    st.divider()

    # --- SEÇÃO 2: DADOS DA EMPRESA ---
    st.subheader("2. Informações da Empresa")
    nome_empresa = st.text_input("Nome Fantasia do Laboratório/Empresa")
    endereco = st.text_input("Endereço Comercial Completo")

    st.divider()

    # --- SEÇÃO 3: PLANO DE ASSINATURA ---
    st.subheader("3. Escolha seu Plano")
    plano = st.radio(
        "Selecione a recorrência:",
        ["Mensal - R$ 199,00", "Semestral - R$ 990,00", "Anual - R$ 1.790,00 (Melhor Valor)"],
        horizontal=True
    )

    st.divider()

    # --- SEÇÃO 4: PAGAMENTO (SIMULAÇÃO ESTILO HOTMART) ---
    st.subheader("4. Forma de Pagamento")
    
    # Exibição visual das bandeiras
    st.write("💳 Aceitamos:")
    st.markdown("🟡 **Mastercard** | 🔵 **Visa** | 🔴 **Elo** | 🟢 **Pix** | 📄 **Boleto**")
    
    metodo = st.selectbox("Selecione o método:", ["Cartão de Crédito", "Pix", "Boleto Bancário"])

    if metodo == "Cartão de Crédito":
        num_cartao = st.text_input("Número do Cartão", placeholder="0000 0000 0000 0000")
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            titular = st.text_input("Nome no Cartão")
        with c2:
            validade = st.text_input("Validade (MM/AA)")
        with c3:
            cvv = st.text_input("CVV", type="password")
    
    elif metodo == "Pix":
        st.info("O QR Code para pagamento será gerado após a finalização do cadastro.")
    
    st.divider()
    
    # Termos
    concordo = st.checkbox("Li e concordo com os Termos de Uso e Política de Privacidade.")
    
    submit = st.form_submit_button("FINALIZAR E ATIVAR MINHA CONTA", use_container_width=True)

if submit:
    if not concordo:
        st.warning("Você precisa aceitar os termos para continuar.")
    elif all([nome_adm, email, senha, nome_empresa, cpf_cnpj]):
        # Aqui enviamos para a função de cadastro
        # Note que passamos os novos campos como metadados ou adicionamos ao banco
        sucesso, msg = db.cadastrar_usuario_completo(
            nome_adm, email, senha, nome_empresa, "ADM", 
            cpf_cnpj, whatsapp, plano, metodo
        )
        
        if sucesso:
            st.success("✨ Cadastro realizado com sucesso! Sua plataforma está sendo configurada.")
            st.balloons()
            st.info("Você receberá um e-mail com as instruções de acesso.")
        else:
            st.error(msg)
    else:
        st.error("Por favor, preencha todos os campos obrigatórios (Marcados com *).")
