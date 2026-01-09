import streamlit as st
from supabase import create_client
import bcrypt
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÕES ---
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def gerar_senha_provisoria():
    alphabet = string.ascii_letters + string.digits + "@#$%"
    return ''.join(secrets.choice(alphabet) for i in range(10))

def enviar_email_acesso(email_destino, nome_empresa, senha_temp, dominio):
    # Insira aqui os dados do seu SMTP (Gmail/Outlook)
    remetente = "seu_suporte@email.com"
    senha_app = "sua_senha_de_app" 
    
    msg = MIMEMultipart()
    msg['Subject'] = f"🚀 Seu acesso ao Lab {nome_empresa} chegou!"
    msg['From'] = f"Suporte Lab Inteligente <{remetente}>"
    msg['To'] = email_destino

    corpo = f"""
    Parabéns! Sua empresa {nome_empresa} já está ativa no sistema.
    
    Acessos:
    - Plataforma: [LINK_DO_SEU_STREAMLIT]
    - Login: {email_destino}
    - Senha Provisória: {senha_temp}
    - Domínio Registrado: {dominio}
    
    A partir de agora, apenas funcionários com o e-mail {dominio} podem ser cadastrados por você.
    """
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha_app)
        server.send_message(msg)
        server.quit()
        return True
    except: return False

# --- INTERFACE DE CHECKOUT ---
st.title("💳 Checkout Laboratórios Inteligentes")

with st.form("checkout"):
    nome_emp = st.text_input("Nome da Empresa")
    email_dono = st.text_input("E-mail do Responsável")
    dominio_escolhido = st.text_input("Domínio da Equipe (Ex: @labtokyo.com)")
    
    st.divider()
    cartao = st.text_input("Número do Cartão", type="password")
    
    if st.form_submit_button("FINALIZAR E RECEBER ACESSOS"):
        if len(cartao) < 16:
            st.error("Pagamento recusado: Verifique os dados do cartão.")
        else:
            # 1. Criar Empresa
            supabase.table("empresas").insert({
                "nome": nome_emp,
                "dominio_customizado": dominio_escolhido.strip().lower()
            }).execute()

            # 2. Criar Usuário ADM
            senha_limpa = gerar_senha_provisoria()
            hashed = bcrypt.hashpw(senha_limpa.encode(), bcrypt.gensalt()).decode()
            
            supabase.table("usuarios").insert({
                "email": email_dono,
                "password": hashed,
                "username": f"ADM {nome_emp}",
                "org_name": nome_emp,
                "role": "ADM"
            }).execute()

            # 3. Enviar E-mail
            if enviar_email_acesso(email_dono, nome_emp, senha_limpa, dominio_escolhido):
                st.success("✅ Sucesso! Verifique seu e-mail para acessar o sistema.")
            else:
                st.warning("Conta criada, mas houve um erro ao enviar o e-mail. Anote sua senha: " + senha_limpa)
