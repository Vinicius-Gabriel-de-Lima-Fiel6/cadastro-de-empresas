import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st

def enviar_email_boas_vindas(email_destino, nome_usuario, nome_empresa):
    # Configurações do Servidor (Exemplo Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = st.secrets["EMAIL_USER"] # Seu e-mail no secrets
    senha = st.secrets["EMAIL_PASS"]     # Sua Senha de App no secrets

    # Variáveis do Sistema
    link_sistema = "https://seusistema.streamlit.app" # Link do seu app principal
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    # Montagem do Corpo do E-mail (Baseado no seu modelo)
    corpo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
            <h2 style="color: #007bff;">Parabéns! 🎉 Sua empresa está cadastrada.</h2>
            <p>Fala, <strong>{nome_usuario}</strong>!</p>
            <p>Seja bem-vindo(a) à nossa plataforma Tech. Ficamos felizes em fazer parte da gestão do <strong>{nome_empresa}</strong>.</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 5px solid #007bff;">
                <h3 style="margin-top: 0;">🚀 Como acessar seu Painel</h3>
                <p>🔗 <strong>Link de Acesso:</strong> <a href="{link_sistema}">{link_sistema}</a></p>
                <p>📧 <strong>Login:</strong> {email_destino}</p>
                <p>🔑 <strong>Senha:</strong> Use a senha cadastrada no momento da inscrição.</p>
                <p style="font-size: 0.8em; color: #666;">Data da Inscrição: {data_hoje}</p>
            </div>

            <p>🚨 <strong>Importante:</strong> Seu acesso é pessoal para o nível administrativo. Caso precise adicionar técnicos ou visualizadores, use a aba "Gestão de Equipe" dentro do sistema.</p>
            
            <h4>🆘 Precisa de Ajuda?</h4>
            <p>Qualquer dúvida sobre o uso do sistema ou suporte técnico, responda a este e-mail ou fale conosco via WhatsApp.</p>
            
            <hr>
            <p style="text-align: center; font-size: 0.8em; color: #999;">
                © {datetime.now().year} Sua Empresa Tech - Todos os Direitos Reservados.
            </p>
        </div>
    </body>
    </html>
    """

    # Configuração da Mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = email_destino
    msg['Subject'] = f"Bem-vindo à Tech - Acesso Liberado: {nome_empresa}"
    msg.attach(MIMEText(corpo_html, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
