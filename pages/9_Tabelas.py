import streamlit as st
import json
from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
import os


st.set_page_config(
    page_title="Tabelas",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto",
)

def encrypt(json_data, password):
    # Convert password to 32 byte AES key
    key = hashlib.sha256(password.encode()).digest()

    # Prepare AES cipher
    cipher = AES.new(key, AES.MODE_EAX)

    # Encrypt data
    ciphertext, tag = cipher.encrypt_and_digest(json_data)

    # Build dictionary to store encryption details
    result = {
        'ciphertext': b64encode(ciphertext).decode('utf-8'),
        'nonce': b64encode(cipher.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

    return result


def decrypt(enc_dict, password):
    # Convert password to 32 byte AES key
    key = hashlib.sha256(password.encode()).digest()

    # Create a new EAX cipher
    cipher = AES.new(key, AES.MODE_EAX, nonce=b64decode(enc_dict['nonce']))

    # Decrypt the data
    decrypted = cipher.decrypt_and_verify(b64decode(enc_dict['ciphertext']),
                                          b64decode(enc_dict['tag']))

    # Convert bytes to string
    decrypted = decrypted.decode('utf-8')

    # Load JSON data from string
    data = json.loads(decrypted)

    return data


def save_encrypted(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


def load_and_decrypt(filename, password):
    with open(filename, 'r') as f:
        enc_data = json.load(f)
    return decrypt(enc_data, password)


def save_decrypted(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    try:
        # Encryption password
        password = st.text_input('Enter the password: ')
        action = st.selectbox(
            'Would you like to encrypt or decrypt?', ('Update', 'Encrypt', 'Decrypt'))

        # Specify the directory path
        directory_path = 'src/tabelas'

        # Get a list of files in the directory
        file_list = sorted([file for file in os.listdir(
            directory_path) if os.path.isfile(os.path.join(directory_path, file))], reverse=True)

        if action == 'Update':
            file_to_update = st.selectbox('Select a file to Update', file_list)
            new_name = st.text_input("New File Name:")
            if file_to_update and password:
                full_file_path = os.path.join(directory_path, file_to_update)
                # Load encrypted data and decrypt it
                decrypted = load_and_decrypt(full_file_path, password)
                dec_str = json.dumps(decrypted, ensure_ascii=False)
                new_file = st.text_area("File to Update", dec_str, height=500)
                new_dict = json.loads(new_file)            

            if st.button("Save"):
                # Save decrypted data
                save_decrypted(
                    new_dict, f'{os.path.join(directory_path, new_name)}upt.json')
                st.toast("Updated")

        elif action == 'Encrypt':

            file_to_encrypt = st.selectbox('Select a file to Encrypt', file_list)
            if file_to_encrypt:
                full_file_path = os.path.join(directory_path, file_to_encrypt)
                # Open the JSON file and load the data
                with open(full_file_path, encoding='utf-8') as f:
                    data = json.load(f)

                # Convert JSON data to string
                json_data = json.dumps(data).encode('utf-8')
                st.text_area("File to Encrypt", json_data, height=500)
            if st.button("Encrypt"):
                # Encrypt data
                encrypted = encrypt(json_data, password)

                # Save encrypted data
                file_to_save = os.path.join(directory_path, "new_encrypted")
                save_encrypted(encrypted, f'{file_to_save}.json')
                st.toast("Encrypted")

        elif action == 'Decrypt':
            file_to_decrypt = st.selectbox('Select a file to Decrypt', file_list)
            if file_to_decrypt and password:
                full_file_path = os.path.join(directory_path, file_to_decrypt)
                # Load encrypted data and decrypt it
                decrypted = load_and_decrypt(full_file_path, password)
                st.text_area("File to Decrypt", decrypted, height=500)
            if st.button("Decrypt"):
                # Save decrypted data
                save_decrypted(decrypted, f'{full_file_path}_dec.json')
                st.toast("Decrypted")
    except Exception as e:
        st.toast("Incorrect Password, try again!", icon="❗")
        print(e)
    

if __name__ == '__main__':
    main()
