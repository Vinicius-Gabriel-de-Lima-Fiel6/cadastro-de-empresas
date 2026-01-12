import streamlit as st
import auth_db as db 

st.title("🧪 Registo de Nova Empresa")

with st.form("form_cadastro_externo"):
    st.markdown("### Dados do Administrador")
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail Profissional")
    senha = st.text_input("Palavra-passe", type="password")
    
    st.markdown("### Dados da Organização")
    empresa = st.text_input("Nome da Empresa/Laboratório")
    
    botao = st.form_submit_button("Criar Conta Empresarial")

if botao:
    if nome and email and senha and empresa:
        # Forçamos o cargo como ADM por ser o cadastro externo
        sucesso, mensagem = db.cadastrar_usuario(nome, email, senha, empresa, "ADM")
        
        if sucesso:
            st.success("✅ Empresa e Administrador registados com sucesso!")
            st.balloons()
            st.info("Já pode aceder ao sistema principal com as suas credenciais.")
        else:
            # Aqui aparecerá o erro de "Empresa já cadastrada"
            st.error(mensagem)
    else:
        st.warning("Por favor, preencha todos os campos do formulário.")
