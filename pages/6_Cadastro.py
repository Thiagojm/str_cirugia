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
action = st.sidebar.selectbox('Choose an action', ['Edit', 'Create', 'Delete'])

# Create a selectbox to choose the directory
directory = st.sidebar.selectbox('Choose a directory', directories)

if action == 'Edit':
    # If the action is Edit, list the files in the chosen directory for editing
    files = list_files_in_directory(directory)
    if files:
        file_to_edit = st.selectbox('Choose a file to edit', files)
        with open(os.path.join(directory, file_to_edit), 'r', encoding="UTF-8") as f:
            content = f.read()
        updated_content = st.text_area('File content', value=content, height=600)
        if st.button('Save changes'):
            create_file(directory, file_to_edit, updated_content)
            st.success('File updated successfully.')
    else:
        st.write('No files in this directory.')

elif action == 'Create':
    # If the action is Create, provide a field to enter the filename and the content
    filename = st.text_input('Enter a filename')
    content = st.text_area('Enter the content', height=600)
    if st.button('Create file'):
        create_file(directory, filename, content)
        st.success('File created successfully.')

elif action == 'Delete':
    # If the action is Delete, list the files in the chosen directory for deletion
    files = list_files_in_directory(directory)
    if files:
        file_to_delete = st.selectbox('Choose a file to delete', files)
        if st.button('Delete file'):
            delete_file(directory, file_to_delete)
            st.success('File deleted successfully.')
    else:
        st.write('No files in this directory.')
