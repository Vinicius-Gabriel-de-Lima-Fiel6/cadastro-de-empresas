import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st

def enviar_email_boas_vindas(email_destino, nome_usuario, nome_empresa):
    # Configurações do Servidor
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = st.secrets["EMAIL_USER"]
    senha = st.secrets["EMAIL_PASS"]

    # Variáveis Dinâmicas
    link_sistema = "https://sistemaparalaboratoriosinteligentes-af2k9rvzo3xemfzmnrjlpr.streamlit.app/"
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    corpo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
            <div style="text-align: center;">
                <h1 style="color: #007bff;">🧪 LabSmartAI</h1>
            </div>
            <h2 style="color: #28a745;">Parabéns! 🎉 Sua licença foi ativada.</h2>
            <p>Fala, <strong>{nome_usuario}</strong>!</p>
            <p>Você acaba de dar um passo importante na inovação do <strong>{nome_empresa}</strong>. Estamos muito felizes em ter você conosco.</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 5px solid #007bff;">
                <h3 style="margin-top: 0;">🚀 Seu Acesso ao Portal</h3>
                <p>🔗 <strong>Link do Sistema:</strong> <a href="{link_sistema}">{link_sistema}</a></p>
                <p>📧 <strong>Login:</strong> {email_destino}</p>
                <p>🔑 <strong>Senha:</strong> A senha que você criou no cadastro.</p>
                <p style="font-size: 0.8em; color: #666;">Data de Ativação: {data_hoje}</p>
            </div>

            <p>🚨 <strong>Atenção:</strong> Como Administrador Único, você já pode acessar o sistema e cadastrar sua equipe na aba "Gestão de Equipe".</p>
            
            <h4>🆘 Precisa de suporte técnico?</h4>
            <p>Fale com nosso time de especialistas:</p>
            <p>🟢 WhatsApp: (61) 9331-4870<br>
               📧 E-mail: {remetente}</p>
            
            <hr>
            <p style="text-align: center; font-size: 0.8em; color: #999;">
                © {datetime.now().year} LabSmartAI Tech - Todos os Direitos Reservados.
            </p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = email_destino
    msg['Subject'] = f"Bem-vindo ao LabSmartAI - Acesso Liberado: {nome_empresa}"
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
