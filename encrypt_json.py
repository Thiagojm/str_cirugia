import json
from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES

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

def main():
    # Encryption password
    password = input('What password would you like to use?: ')

    file_to_encrypt = input('What file would you like to encrypt?: ')
    # Open the JSON file and load the data
    with open(file_to_encrypt, encoding='utf-8') as f:
        data = json.load(f)

    # Convert JSON data to string
    json_data = json.dumps(data).encode('utf-8')

    # Encrypt data
    encrypted = encrypt(json_data, password)

    print("Encrypted:", encrypted)

    # Save encrypted data
    save_encrypted(encrypted, f'data/{file_to_encrypt}_enc.json')

    # Load encrypted data and decrypt it
    decrypted = load_and_decrypt(f'data/{file_to_encrypt}_enc.json', password)

    print("Decrypted:", decrypted)

if __name__ == '__main__':
    main()
