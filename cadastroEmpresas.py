import streamlit as st
from supabase import create_client
import bcrypt
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÕES DE CONEXÃO ---
# Certifique-se de que estas chaves estão nos "Secrets" do Streamlit
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNÇÕES DE APOIO ---
def gerar_senha_provisoria():
    """Gera uma senha forte para o primeiro acesso"""
    alphabet = string.ascii_letters + string.digits + "@#$%"
    return ''.join(secrets.choice(alphabet) for i in range(10))

def enviar_email_acesso(email_destino, nome_empresa, senha_temp, dominio):
    """Envia o e-mail com as credenciais (Opcional: Requer SMTP configurado)"""
    # Se ainda não tiver as senhas de app do Google, o código apenas mostrará na tela
    remetente = "seu_suporte@email.com"
    senha_app = "sua_senha_de_app" 
    
    msg = MIMEMultipart()
    msg['Subject'] = f"🚀 Seu acesso ao Lab {nome_empresa} chegou!"
    msg['From'] = f"Suporte Lab Inteligente <{remetente}>"
    msg['To'] = email_destino

    corpo = f"Sua empresa {nome_empresa} está ativa. Login: {email_destino} | Senha: {senha_temp} | Domínio: {dominio}"
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha_app)
        server.send_message(msg)
        server.quit()
        return True
    except: return False

# --- INTERFACE DO CHECKOUT ---
st.set_page_config(page_title="Ativação de Instância", page_icon="💳")

st.title("💳 Finalizar Assinatura")
st.write("Configure sua empresa e receba os acessos instantaneamente.")

with st.form("checkout_form"):
    st.subheader("1. Dados da Organização")
    nome_emp = st.text_input("Nome da Empresa / Laboratório", placeholder="Ex: Lab Tokyo")
    email_dono = st.text_input("E-mail do Administrador Master")
    dominio_escolhido = st.text_input("Padrão de e-mail da equipe", placeholder="Ex: @labtokyo.com")
    plano_selecionado = st.selectbox("Plano", ["Mensal", "Anual"])
    
    st.divider()
    st.subheader("2. Pagamento Simulado")
    cartao = st.text_input("Número do Cartão (Use 16 dígitos para testar)", type="password")
    
    botao_ativar = st.form_submit_button("ATIVAR MINHA EMPRESA AGORA")

if botao_ativar:
    # Validação simples de preenchimento
    if not nome_emp or not email_dono or not dominio_escolhido:
        st.error("Por favor, preencha todos os campos da empresa.")
    elif len(cartao.replace(" ", "")) < 16:
        st.error("Pagamento recusado: O cartão deve ter 16 dígitos.")
    else:
        try:
            # --- PASSO 1: CRIAR A EMPRESA ---
            # O ID é gerado automaticamente pelo banco (gen_random_uuid())
            res_empresa = supabase.table("empresas").insert({
                "nome": nome_emp,
                "dominio_customizado": dominio_escolhido.strip().lower(),
                "status_assinatura": "Ativo",
                "plano": plano_selecionado
            }).execute()

            # --- PASSO 2: CRIAR O USUÁRIO MASTER ---
            senha_limpa = gerar_senha_provisoria()
            hashed_pw = bcrypt.hashpw(senha_limpa.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            supabase.table("usuarios").insert({
                "email": email_dono.strip().lower(),
                "password": hashed_pw,
                "username": f"Master {nome_emp}",
                "org_name": nome_emp, # FK para a tabela empresas
                "role": "ADM",
                "primeiro_acesso": True
            }).execute()

            # --- PASSO 3: SUCESSO E EXIBIÇÃO ---
            st.balloons()
            st.success("✅ Empresa provisionada com sucesso!")
            
            st.info(f"""
            ### 🔑 Seus Acessos:
            - **Empresa:** {nome_emp}
            - **Login:** {email_dono}
            - **Senha Temporária:** `{senha_limpa}`
            - **Domínio Autorizado:** `{dominio_escolhido}`
            
            *Anote sua senha. Ela será solicitada no primeiro login no Sistema B.*
            """)
            
            # Tenta enviar e-mail (se falhar, a senha já está na tela acima)
            enviar_email_acesso(email_dono, nome_emp, senha_limpa, dominio_escolhido)

        except Exception as e:
            # Se der erro aqui, geralmente é nome de empresa duplicado ou erro de RLS
            st.error(f"Erro crítico ao salvar no banco: {e}")
            st.info("Verifique se o nome da empresa já existe ou se as POLICIES do SQL foram rodadas.")
