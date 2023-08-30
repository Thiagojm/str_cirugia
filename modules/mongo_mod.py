import streamlit as st
from pymongo import MongoClient


CONN_STRING = st.secrets['mongodb_cred']["conn_string"]

# Initialize connection.
# Uses st.cache_resource to only run once.


@st.cache_resource
def init_connection():
    return MongoClient(CONN_STRING)


# Create a connection using MongoClient
# client = init_connection()

# Connect to the desired database
# db = client.my_test_db


def list_collections(db):
    """
    Lists all collections in the database sorted alphabetically.

    Returns:
    - list: List of collection names sorted alphabetically.
    """

    collections = db.list_collection_names()
    return sorted(collections)


def update_document_content_by_field(db, collection_name, field_name, new_value):
    """
    Updates the content of a field within all documents that have the specified field_name.

    Parameters:
    - collection_name (str): The name of the collection.
    - field_name (str): The field's name used to match and update the document.
    - new_value (any): The new value to update within the document's field.

    Returns:
    - int: The number of documents updated.
    """

    collection = db[collection_name]

    result = collection.update_many({field_name: {"$exists": True}}, {
                                    "$set": {field_name: new_value}})

    return result.modified_count


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
        st.toast(
            f"A document with the field name '{field_name}' already exists.", icon="❌")
        return None

    collection = db[collection_name]
    document = {field_name: content}

    try:
        result = collection.insert_one(document)
        if result:
            return result

    except Exception as e:
        st.toast(f"An unexpected error occurred: {e}", icon="❗")

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
        st.toast("No document found.", icon="❗")
        return None


def delete_document(db, collection_name, field_name):
    """
    Deletes a document based on the specified field_name and its value.

    Parameters:
    - collection_name (str): The name of the collection.
    - field_name (str): The field's name used to match the document.
    - value (any): The value associated with the field_name used to match the document.

    Returns:
    - bool: True if a document was deleted, False otherwise.
    """

    collection = db[collection_name]

    result = collection.delete_one({field_name: {"$exists": True}})

    return result.deleted_count > 0


def list_field_names(db, collection_name):
    """
    Lists distinct field names from all documents within the collection.
    Results are sorted alphabetically.

    Parameters:
    - collection_name (str): The name of the collection.

    Returns:
    - list: List of distinct field names sorted alphabetically.
    """

    collection = db[collection_name]

    # Use aggregation to get all field names from the collection
    pipeline = [
        {"$project": {"arrayofkeyvalue": {"$objectToArray": "$$ROOT"}}},
        {"$unwind": "$arrayofkeyvalue"},
        {"$group": {"_id": None, "allKeys": {"$addToSet": "$arrayofkeyvalue.k"}}}
    ]

    result = list(collection.aggregate(pipeline))

    if result:
        field_names = result[0]["allKeys"]
    else:
        field_names = []

    # Remove '_id' from the list
    field_names = [name for name in field_names if name != "_id"]

    return sorted(field_names)

# is_deleted = delete_document(db, "test_col", "Mupirocinaaa")
# if is_deleted:
#     print("Document was successfully deleted.")
# else:
#     print("No document matched the criteria.")

# Example usage:
# result = insert_one_document(db, "test_col", "Mupirocinaaa", "Prótese, orçamento, à, ")

# updated_count = update_document_content_by_field(db, "test_col", "Mupirodfscina", "mudou")
# print(f"{updated_count} documents were updated.")

# content = get_document_content(db, "test_col", "Mupirocinaaa")
# print(content)

# collections = list_collections(db)
# print("Collections in the database:", collections)

# fields = list_field_names(db, "test_col")
# print("Field names in the collection:", fields)
