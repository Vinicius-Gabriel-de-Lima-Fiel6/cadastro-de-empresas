import streamlit as st
from supabase import create_client, Client
import bcrypt

# --- Conexão ---
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Erro de conexão com o banco: {e}")

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def cadastrar_usuario_completo(username, email, senha_limpa, org_name, role, cpf, whatsapp, plano, metodo):
    global supabase
    try:
        senha_protegida = hash_senha(senha_limpa)
        
        # 1. Trava de Unicidade da Empresa
        check_org = supabase.table("organizations").select("id").eq("name", org_name).execute()
        if check_org.data:
            return False, f"A empresa '{org_name}' já está cadastrada."

        # 2. Criação da Organização
        org_payload = {
            "name": org_name,
            "plano_ativo": plano,
            "metodo_pagto": metodo,
            "status_assinatura": "ativo"
        }
        res_org = supabase.table("organizations").insert(org_payload).execute()
        org_id = res_org.data[0]['id']

        # 3. Criação do Usuário ADM
        user_payload = {
            "username": username,
            "email": email,
            "password_hash": senha_protegida,
            "org_name": org_name,
            "org_id": org_id,
            "role": role,
            "cpf_cnpj": cpf,
            "whatsapp": whatsapp
        }
        
        supabase.table("users").insert(user_payload).execute()
        return True, "Sucesso"

    except Exception as e:
        return False, f"Erro no processamento: {str(e)}"
