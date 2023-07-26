import streamlit as st
import os
import streamlit_authenticator as stauth
import qmod as qm

# Define the directories to look into
directories = ['src/atestados', 'src/laudos', 'src/receitas', 'src/termos']

def list_files_in_directory(directory):
    # List all files in the given directory
    return sorted([os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

def create_file(directory, filename, content):
    # Create a new file in the given directory with the given content
    with open(os.path.join(directory, filename + '.txt'), 'w', encoding="UTF-8") as f:
        f.write(content)

def delete_file(directory, filename):
    # Delete the specified file
    os.remove(os.path.join(directory, filename + '.txt'))

def main():
     # Create or get the session state
    if "session" not in st.session_state:
        st.session_state.session = qm.SessionState()
        
    if 'patient_name' not in st.session_state:
        st.session_state['patient_name'] = ''  

    if 'cirurgia_name' not in st.session_state:
        st.session_state['cirurgia_name'] = ''  
    
    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")
    # Create a selectbox to choose the action
    action = st.sidebar.selectbox('Selecione uma ação', ['Editar', 'Criar', 'Deletar'])

    # Create a selectbox to choose the directory
    directory_mapping = {os.path.basename(dir): dir for dir in directories}
    directory = st.sidebar.selectbox('Selecione um diretório', list(directory_mapping.keys()))

    if action == 'Editar':
        # If the action is Edit, list the files in the chosen directory for editing
        files = list_files_in_directory(directory_mapping[directory])
        if files:
            file_to_edit = st.selectbox('Escolha um arquivo para editar', files)
            with open(os.path.join(directory_mapping[directory], file_to_edit + '.txt'), 'r', encoding="UTF-8") as f:
                content = f.read()
            updated_content = st.text_area('Conteúdo do Arquivo', value=content, height=600)
            if st.button('Salvar modificações'):
                create_file(directory_mapping[directory], file_to_edit, updated_content)
                st.success('Arquivo editado com sucesso')
        else:
            st.write('Sem arquivos nesse diretório')

    elif action == 'Criar':
        # If the action is Create, provide a field to enter the filename and the content
        filename = st.text_input('Nome do arquivo')
        content = st.text_area('Conteúdo', height=600)
        if st.button('Criar arquivo'):
            create_file(directory_mapping[directory], filename, content)
            st.success('Arquivo criado com sucesso')

    elif action == 'Deletar':
        # If the action is Delete, list the files in the chosen directory for deletion
        files = list_files_in_directory(directory_mapping[directory])
        if files:
            file_to_delete = st.selectbox('Selecione um arquivo para deletar', files)
            if st.button('Deletar arquivo'):
                delete_file(directory_mapping[directory], file_to_delete)
                st.success('Arquivo deletado com sucesso.')
        else:
            st.write('Sem arquivos nesse diretório.')
            

if __name__ == "__main__":
     # Create an instance of the Authenticate class
    authenticator = stauth.Authenticate(
    dict(st.secrets['credentials']),
    st.secrets['cookie']['name'],
    st.secrets['cookie']['key'],
    st.secrets['cookie']['expiry_days'],
    st.secrets['preauthorized']
)
    table_pass = st.secrets['table_pass']["pass"]
    
    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        main()