import streamlit as st
import os

# Define the directories to look into
directories = ['src/atestados', 'src/laudos', 'src/receitas', 'src/termos']

def list_files_in_directory(directory):
    # List all files in the given directory
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def create_file(directory, filename, content):
    # Create a new file in the given directory with the given content
    with open(os.path.join(directory, filename), 'w') as f:
        f.write(content)

def delete_file(directory, filename):
    # Delete the specified file
    os.remove(os.path.join(directory, filename))

# Create a selectbox to choose the action
action = st.sidebar.selectbox('Choose an action', ['Editar', 'Criar', 'Deletar'])

# Create a selectbox to choose the directory
directory = st.sidebar.selectbox('Choose a directory', directories)

if action == 'Editar':
    # If the action is Edit, list the files in the chosen directory for editing
    files = list_files_in_directory(directory)
    if files:
        file_to_edit = st.selectbox('Escolha um arquivo para editar', files)
        with open(os.path.join(directory, file_to_edit), 'r', encoding="UTF-8") as f:
            content = f.read()
        updated_content = st.text_area('Conteúdo do Arquivo', value=content, height=600)
        if st.button('Salvar modificações'):
            create_file(directory, file_to_edit, updated_content)
            st.success('Arquivo editado com sucesso')
    else:
        st.write('Sem arquivos nesse diretório')

elif action == 'Criar':
    # If the action is Create, provide a field to enter the filename and the content
    filename = st.text_input('Nome do arquivo (coloque .txt no final)')
    content = st.text_area('Conteúdo', height=600)
    if st.button('Criar arquivo'):
        create_file(directory, filename, content)
        st.success('Arquivo criado com sucesso')

elif action == 'Deletar':
    # If the action is Delete, list the files in the chosen directory for deletion
    files = list_files_in_directory(directory)
    if files:
        file_to_delete = st.selectbox('Selecione um arquivo para deletar', files)
        if st.button('Deletar arquivo'):
            delete_file(directory, file_to_delete)
            st.success('Arquivo deletado com sucesso.')
    else:
        st.write('Sem arquivos nesse diretório.')
