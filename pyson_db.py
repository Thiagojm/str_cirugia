from pysondb import db

# create or get the db
atestados = db.getDb("atestados.json")

# add to database
def add_db(db, doc_name, text):
    if not check_doc(db, doc_name):
        print("Doc already in db, select another name or update it.")
    else:
        db.add({"name":doc_name, "text": text})
        print("Doc Saved.")

# check if doc exists
def check_doc(db, doc_name):
    checked = db.getByQuery({"name": doc_name})
    if checked:
        # if found return id
        return checked[0]["id"]
    else:
        return False

# get text from doc
def get_text(db, doc_name):
    if check_doc(db, doc_name):
        text = db.getByQuery({"name": doc_name})
        return text[0]["text"]
    else:
        print("Doc does not exist.")
        return None
    
# update the doc text    
def update_doc(db, doc_name, new_text):
    if check_doc(db, doc_name):
        db.updateByQuery({"name":doc_name}, {"text":new_text})
        print("Doc updated.")
    else:
        print("Doc does not exist.")


# delete document    
def delete_doc(db, doc_name):
    doc_id = check_doc(db, doc_name)
    if doc_id:
        db.deleteById(doc_id)
        print("Doc deleted.")
    else:
        print("Doc does not exist.")
        
delete_doc(atestados, "a5")       
        
#update_doc(atestados, "Atestadohfg", "ajshdkjasd")
    
#print(get_text(atestados, "Atestado"))

#add_db(atestados, "a5", "puriko")

# Update db
# a.updateByQuery({"name":"Atestado2"}, {"text": "Outro atestado"})

#print(check_doc(atestados, {"name":"Atestado4"}))
