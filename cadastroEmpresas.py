import streamlit as st
import auth_db as db 

st.set_page_config(page_title="Cadastro LabSmartAI", page_icon="🧪")

st.title("🧪 Portal de Cadastro LabSmartAI")
st.write("Crie sua conta para acessar a plataforma principal.")

with st.container():
    st.info("O primeiro cadastro cria a Organização e define o Administrador (ADM).")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Seu Nome Completo")
        new_email = st.text_input("E-mail Corporativo")
        new_pass = st.text_input("Senha", type="password")
    with col2:
        new_org = st.text_input("Nome da Empresa/Laboratório")
        st.warning("Cargo padrão: ADM")
    
    if st.button("Finalizar Cadastro", use_container_width=True):
        if new_email and new_pass and new_org:
            # Chama a função original do auth_db
            sucesso, msg = db.cadastrar_usuario(new_name, new_email, new_pass, new_org, "ADM")
            if sucesso:
                st.success(f"{msg} Você já pode fazer login no site principal.")
                st.balloons()
            else:
                st.error(msg)
        else:
            st.warning("Preencha todos os campos.")
