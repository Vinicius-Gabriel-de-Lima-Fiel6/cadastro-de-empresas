import streamlit as st
from supabase import create_client
import bcrypt
import secrets

# Conexão
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("🚀 Ativação de Empresa")

with st.form("ativacao"):
    nome_emp = st.text_input("Nome da Empresa")
    email_adm = st.text_input("E-mail do Administrador")
    dominio = st.text_input("Domínio da Equipe (Ex: @lab.com)")
    plano = st.selectbox("Plano", ["Mensal", "Anual"])
    cartao = st.text_input("Cartão (16 dígitos)", type="password")
    
    if st.form_submit_button("ATIVAR AGORA"):
        if len(cartao.replace(" ","")) == 16:
            try:
                # 1. SALVAR EMPRESA
                # O banco gera o UUID sozinho, então não enviamos 'id'
                supabase.table("empresas").insert({
                    "nome": nome_emp,
                    "dominio_customizado": dominio.strip().lower(),
                    "status_assinatura": "Ativo",
                    "plano": plano
                }).execute()

                # 2. SALVAR USUÁRIO MASTER
                senha_temp = "".join(secrets.choice("ABCDEF123456") for i in range(8))
                hashed = bcrypt.hashpw(senha_temp.encode(), bcrypt.gensalt()).decode()

                supabase.table("usuarios").insert({
                    "email": email_adm.strip().lower(),
                    "password": hashed,
                    "username": "Administrador Master",
                    "org_name": nome_emp,
                    "role": "ADM",
                    "primeiro_acesso": True
                }).execute()

                st.success(f"✅ Empresa Ativada! Senha de acesso: {senha_temp}")
                st.balloons()

            except Exception as e:
                st.error(f"Erro no banco: {e}")
        else:
            st.error("Cartão inválido!")
