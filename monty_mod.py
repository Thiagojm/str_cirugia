from montydb import MontyClient


def insert_document(client, key, value):
    check = find_document(client, key)
    if check:
        print("Document already in db, choose new name or update it.")
    else:
        client.insert_one({key: value})
        print("Document saved.")
    
def update_document(client, key, value):
    result = client.update_one({key: {"$exists": True}}, {"$set": {key: value}})
    if result.modified_count != 0:
        print("Success!")
    else:
        print("No such document!")

def find_document(client, key):
    # Fetching one document
    doc = client.find_one({key: {"$exists": True}})

    # To assign the value of 'your_key' to a variable
    if doc and key in doc:  # Make sure the document exists and it has 'your_key'
        value = doc[key]  
        return value
    else:
        print("No such document!")
        return ""

def delete_document(client, key):
    result = client.delete_one({key: {"$exists": True}}) # Delete one document
    if result.deleted_count != 0:
        print("Success!")
    else:
        print("No such document!")

client = MontyClient()
db = client.get_database("db") # Get a database named "db"
receitas = db.get_collection("receitas") # receitas
atestados = db.get_collection("atestados") # receitas

insert_document(atestados, "atestado", "Piruko gato, prótese, ção ã à ;'&^%")

doc_to_update = "trabaaaaaada"
#update_document(atestados, "atestado", doc_to_update)

#delete_document(atestados, "atestado")

#text = find_document(atestados, "atestado")
#print(text)




