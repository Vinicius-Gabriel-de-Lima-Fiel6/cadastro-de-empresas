import streamlit as st
from supabase import create_client
import bcrypt
import secrets

# Conexão com o banco (Chaves devem estar nos Secrets do Streamlit)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("🚀 Ativação de Nova Empresa")

with st.form("form_ativacao"):
    nome_emp = st.text_input("Nome da Empresa")
    email_adm = st.text_input("E-mail do Administrador Master")
    dominio = st.text_input("Domínio de E-mail da Equipe (Ex: @lab.com)")
    plano = st.selectbox("Escolha o Plano", ["Mensal", "Anual"])
    cartao = st.text_input("Número do Cartão (16 dígitos)", type="password")
    
    if st.form_submit_button("ATIVAR MINHA EMPRESA AGORA"):
        # Simulação de pagamento (16 dígitos)
        if len(cartao.replace(" ", "")) == 16:
            try:
                # 1. CRIAR EMPRESA
                # Omitimos o 'id' pois o banco gera o UUID automaticamente
                supabase.table("empresas").insert({
                    "nome": nome_emp,
                    "dominio_customizado": dominio.strip().lower(),
                    "status_assinatura": "Ativo",
                    "plano": plano
                }).execute()

                # 2. CRIAR USUÁRIO MASTER
                senha_temp = "".join(secrets.choice("ABCDEF123456789") for i in range(8))
                salt = bcrypt.gensalt()
                hashed_pw = bcrypt.hashpw(senha_temp.encode(), salt).decode()

                supabase.table("usuarios").insert({
                    "email": email_adm.strip().lower(),
                    "password": hashed_pw,
                    "username": "Administrador Master",
                    "org_name": nome_emp,
                    "role": "ADM",
                    "primeiro_acesso": True
                }).execute()

                st.success(f"✅ Sucesso! Empresa '{nome_emp}' ativada.")
                st.info(f"🔑 Sua senha temporária é: {senha_temp}")
                st.balloons()

            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.error("Cartão inválido! Use 16 números para o teste.")
