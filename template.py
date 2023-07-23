from string import Template


class MyTemplate(Template):
    delimiter = '&'

def change_template(patient_name, cirurgia_name):
    
    d = {
    'patient_name': patient_name,
    'cirurgia_name': cirurgia_name
    }
    with open('scr/termos/Termo Geral.txt', 'r', encoding="UTF-8") as f:
        src = MyTemplate(f.read())    
        termo_result = src.substitute(d)
        
    return termo_result
    



