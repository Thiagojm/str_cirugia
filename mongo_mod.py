from distutils import errors
import streamlit as st
from pymongo import MongoClient

MONGO_LOGIN = st.secrets['mongodb_cred']["username"]
MONGO_PASS = st.secrets['mongodb_cred']["password"]
CONN_STRING = f"mongodb+srv://{MONGO_LOGIN}:{MONGO_PASS}@dr-tjm.imrc7i8.mongodb.net/?retryWrites=true&w=majority"


# Create a connection using MongoClient
client = MongoClient(CONN_STRING)

# Connect to the desired database
db = client.my_test_db  # replace "myFirstDatabase" with your database name

def insert_one_document(db, collection_name, field_name, content):
    """
    Inserts one document into a specified MongoDB Atlas collection.

    Parameters:
    - collection_name (str): The name of the collection.
    - field_name (str): The field's name where content will be stored.
    - content (any): The content/data to be stored in the field.
    
    Returns:
    - result (InsertOneResult or None): The result of the insertion operation or None in case of an error.
    """
    
    if document_exists(db, collection_name, field_name):
        print(f"A document with the field name '{field_name}' already exists.")
        return None
    
    collection = db[collection_name]
    document = {field_name: content}
    
    try:
        result = collection.insert_one(document)
        if result:
            print("Inserted document with id:", result.inserted_id)
            return result
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def document_exists(db, collection_name, field_name):
    """
    Checks if a document with the specified field_name exists in the collection.

    Parameters:
    - collection_name (str): The name of the collection.
    - field_name (str): The field's name to check existence.
    
    Returns:
    - bool: True if the document exists, False otherwise.
    """
    
    collection = db[collection_name]
    existing_document = collection.find_one({field_name: {"$exists": True}})
    return bool(existing_document)

def get_document_content(db, collection_name, field_name):
    """
    Fetches the content of a document based on the specified field_name.

    Parameters:
    - collection_name (str): The name of the collection.
    - field_name (str): The field's name whose content is to be fetched.
    
    Returns:
    - content (any or None): The content of the field or None if the field doesn't exist in any document.
    """
    
    collection = db[collection_name]
    document = collection.find_one({field_name: {"$exists": True}})
    
    if document:
        content = document[field_name]
        return content
    else:
        print("No document found.")
        return None

# Example usage:
# result = insert_one_document(db, "test_col", "Mupirocina", """Uso Externo

# 1- Mupirocina pomada -------------------------------- 1u
# Aplicar nas regiões indicadas de 12/12h""")
content = get_document_content(db, "test_col", "Muplirocina")
print(content)
