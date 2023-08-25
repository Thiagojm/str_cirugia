import streamlit as st
import os
import streamlit_authenticator as stauth
from mongo_mod import *


def main():

    if 'patient_name' not in st.session_state:
        st.session_state['patient_name'] = ''

    if 'cirurgia_name' not in st.session_state:
        st.session_state['cirurgia_name'] = ''

    # Start Db
    # Create a connection using MongoClient
    client = init_connection()

    # Connect to the desired database
    db = client.drtjm
    
    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")

    st.title('Cadastros')

    # Create a selectbox to choose the action
    action = st.selectbox(
        'Selecione uma ação', ['Editar', 'Criar', 'Deletar'])

    # Create a selectbox to choose the directory
    directory_mapping = list_collections(db)
    directory = st.selectbox(
        'Selecione um diretório', directory_mapping)

    if action == 'Editar':
        # If the action is Edit, list the files in the chosen directory for editing
        files = list_field_names(db, directory)
        if files:
            file_to_edit = st.selectbox(
                'Escolha um arquivo para editar', files)
            content = get_document_content(db, directory, file_to_edit)
            updated_content = st.text_area(
                'Conteúdo do Arquivo', value=content, height=500)
            if st.button('Salvar modificações'):
                num_edited = update_document_content_by_field(db, directory, file_to_edit, updated_content)
                st.toast(f'{num_edited} arquivo editado com sucesso', icon="✔️")
        else:
            st.write('Sem arquivos nesse diretório')

    elif action == 'Criar':
        # If the action is Create, provide a field to enter the filename and the content
        filename = st.text_input('Nome do arquivo')
        content = st.text_area('Conteúdo', height=500)
        if st.button('Criar arquivo'):
            insterted = insert_one_document(db, directory, filename, content)
            if insterted:
                st.toast('Arquivo criado com sucesso', icon="✔️")

    elif action == 'Deletar':
        # If the action is Delete, list the files in the chosen directory for deletion
        files = list_field_names(db, directory)
        if files:
            file_to_delete = st.selectbox(
                'Selecione um arquivo para deletar', files)
            if st.button('Deletar arquivo'):
                num_deleted = delete_document(db, directory, file_to_delete)
                if num_deleted:
                    st.toast('Arquivo deletado com sucesso.', icon="✔️")
        else:
            st.toast("Something went wrong.", icon="❗")


if __name__ == "__main__":
    # Create an instance of the Authenticate class
    authenticator = stauth.Authenticate(
        dict(st.secrets['credentials']),
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days'],
        st.secrets['preauthorized']
    )

    name, authentication_status, username = authenticator.login(
        "Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        main()
