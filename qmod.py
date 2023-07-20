import streamlit as st
import json
from base64 import b64decode
import hashlib
from Crypto.Cipher import AES
      
# Define a class to handle session state
class SessionState:
    def __init__(self):
        self.messages = []


def load_and_decrypt(filename, password):
    with open(filename, 'r') as f:
        enc_data = json.load(f)
    return decrypt(enc_data, password)

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

# Define a função calculate
def calculate(checked_boxes, extra_values, data):
    try:
        nome_cirurgia = checked_boxes
        extras = extra_values
        valor_protese = float(extras[1].replace(",", "."))
        tempo_lipo = float(extras[2].replace(",", "."))
        tipo_protese = extras[7]
        if not nome_cirurgia:
            st.error(f"Nenhuma cirurgia selecionada, tente novamente")
            return ""
        if "Lipoescultura(2,5h)" in nome_cirurgia:
            if tempo_lipo == 0:
                tempo_lipo = 2.5
        elif "Lipoescultura(3h)" in nome_cirurgia:
            if tempo_lipo == 0:
                tempo_lipo = 3.5
        elif "Lipoaspiração" in nome_cirurgia and tempo_lipo == 0:
            st.warning("Escolha o tempo de lipoaspiração")
            return ""
        if "Mamoplastia com Prótese" in nome_cirurgia or "Prótese de Mama" in nome_cirurgia:
            tipo_protese = extras[7]
            if valor_protese == 0:
                valor_protese = int(data["PROTESES"][tipo_protese])
        ajuste_q = extras[0]
        tempo, diaria = tempo_diaria(
            nome_cirurgia, data["CIRURGIAS_EQUIPE"], data["LIPO_MENOS_1H"], tempo_lipo
        )
        if extras[3] != "0":
            tempo = int(extras[3])
        if extras[4]:
            diaria = int(extras[4])
        valor_equipe_cirurgia = valor_equipe(
            nome_cirurgia, data["CIRURGIAS_EQUIPE"], ajuste_q, tempo_lipo
        )
        valor_anestesista_foz = valor_anestesia_foz(
            nome_cirurgia, tempo_lipo, data["ANESTESIA_FOZ"]
        )
        valor_anestesia_renata = calc_anestesia_renata(
            nome_cirurgia, data["ANESTESIA_RENATA"], data["RENATA_CONS_MENOS"])

        if extras[5] != "0":
            valor_anestesista_foz = int(extras[5])
            valor_anestesia_renata = int(extras[5])

        if extras[6] != "0":
            valor_equipe_cirurgia = int(extras[6])
        
        valor_hosp_hmcc = valor_hmcc(tempo, diaria, data["HMCC"])
        valor_hosp_unimed = valor_unimed(tempo, diaria, data["UNIMED"])
        valor_hosp_hmd = valor_hmd(tempo, diaria, data["HMD"])
        valor_total_hmcc = valor_equipe_cirurgia + \
            valor_anestesista_foz + valor_hosp_hmcc
        valor_total_unimed = (
            valor_equipe_cirurgia + valor_anestesista_foz + valor_hosp_unimed
        )
        valor_total_hmd = valor_equipe_cirurgia + \
            valor_anestesia_renata + valor_hosp_hmd
        print_cir = " , ".join(nome_cirurgia)
        message = ""
        message = " \n".join([message, f"Cirurgia(s) a ser(em) realizada(s): {print_cir} "])    
        message = " \n".join([message, f"Tempo total de sala: {tempo} horas "])
        message = " \n".join([message, f"Dias de internamento: {diaria} "])
        message = " \n".join([message, f"Valor da equipe: {valor_equipe_cirurgia} "])
        message = " \n".join([message, f"Valor da anestesia HMCC/ Unimed: {valor_anestesista_foz} "])
        # message = " \n".join([message, f"Valor da anestesia HMD: {valor_anestesia_renata} "])
        if valor_protese != 0:
            valor_total_hmcc += valor_protese
            valor_total_unimed += valor_protese
            valor_total_hmd += valor_protese
            message = " \n".join([message, f"Valor da prótese {tipo_protese}: {valor_protese} "])
        if tempo_lipo > 0:
            message = " \n".join([message, f"Tempo de Lipo: {tempo_lipo} horas "])
        # message = " \n".join([message, f"Valor do hospitalar HMD: {valor_hosp_hmd} "])    
        message = " \n".join([message, f"Valor do hospitalar Unimed: {valor_hosp_unimed} "])
        message = " \n".join([message, f"Valor do hospitalar HMCC: {valor_hosp_hmcc} "])
        # message = " \n".join([message, f"Valor total HMD: {valor_total_hmd} "])
        message = " \n".join([message, f"Valor total Unimed: {valor_total_unimed} "])
        message = " \n".join([message, f"Valor total HMCC: {valor_total_hmcc} "])
        message = " \n".join([message, "\n" + "#" * 29 + "\n" ])
        return message
    except Exception as e:
        st.error(f"Prencha todos os campos ou deixe em '0'.\nErro: {e}")
        print(e)


def calc_anestesia_renata(nome_cirurgia, anestesia_renata, renata_cons_menos):
    nome_cirurgia.sort()
    cirurgias = ', '.join(nome_cirurgia)
    valor = anestesia_renata.get(cirurgias) or 0
    if cirurgias in renata_cons_menos:
        valor += anestesia_renata["Consulta-"]
    else:
        valor += anestesia_renata["Consulta"]
    return valor


def valor_equipe(nome_cirurgia, equipe_cirurgias, ajuste_q, tempo_lipo):
    valor = 0

    for i in nome_cirurgia:
        cirurgia = i
        if i == "Lipoaspiração":
            valor += equipe_cirurgias[cirurgia]["valor"] * tempo_lipo
        else:
            valor += equipe_cirurgias[cirurgia]["valor"]
    valor_ajustado = ajuste_func(ajuste_q, valor)
    return round(valor_ajustado, 2)


def ajuste_func(ajuste_q, valor):
    if not ajuste_q:
        ajuste_q = "0"
    if "," in ajuste_q:
        ajuste_q = ajuste_q.replace(",", ".")
    if "%" in ajuste_q:
        ajuste_q = float(ajuste_q[:-1]) / 100
        return valor * (ajuste_q + 1)
    else:
        ajuste_q = float(ajuste_q)
        return valor + ajuste_q


def valor_anestesia_foz(nome_cirurgia, tempo_lipo, anestesia_foz):
    dict_valores = {}
    for i in nome_cirurgia:
        dict_valores[i] = anestesia_foz[i]
    sorted_dict = dict(
        sorted(dict_valores.items(), key=lambda item: item[1], reverse=True)
    )
    lista_cir = list(sorted_dict.keys())
    lista_valores = list(sorted_dict.values())
    if (
        lista_cir[0] == "Lipoescultura(2,5h)"
        or lista_cir[0] == "Lipoaspiração"
        or lista_cir[0] == "Lipoescultura(3h)"
    ):
        lista_valores[0] = lista_valores[0] + (
            (lista_valores[0] / 2) * (tempo_lipo - 1)
        )
    elif "Lipoaspiração" in sorted_dict:
        sorted_dict["Lipoaspiração"] = sorted_dict["Lipoaspiração"] * tempo_lipo
        lista_valores = list(sorted_dict.values())
    elif "Lipoescultura(2,5h)" in sorted_dict:
        sorted_dict["Lipoescultura(2,5h)"] = (
            sorted_dict["Lipoescultura(2,5h)"] * tempo_lipo
        )
        lista_valores = list(sorted_dict.values())
    elif "Lipoescultura(3h)" in sorted_dict:
        sorted_dict["Lipoescultura(3h)"] = sorted_dict["Lipoescultura(3h)"] * tempo_lipo
        lista_valores = list(sorted_dict.values())
    valor = lista_valores[0]
    lista_valores.pop(0)
    for i in lista_valores:
        valor += i / 2
    return valor


def valor_hmcc(tempo, diaria, hmcc):
    return hmcc[str(tempo)][str(diaria)]


def valor_unimed(tempo, diaria, unimed):
    return unimed[str(tempo)][str(diaria)]


def valor_hmd(tempo, diaria, hmd):
    return hmd[str(tempo)][str(diaria)]


def tempo_diaria(nome_cirurgia, equipe_cirurgias, lipo_menos_1h, tempo_lipo):
    tempo = 0
    diaria = 0
    for i in nome_cirurgia:
        tempo += equipe_cirurgias[i]["tempo"]
        diaria += equipe_cirurgias[i]["diaria"]
    if tempo >= 6:
        tempo = 6
    if diaria >= 2:
        diaria = 1
    if "Lipoescultura(2,5h)" in nome_cirurgia or "Lipoescultura(3h)" in nome_cirurgia:
        if len(nome_cirurgia) == 2:
            if any(x in nome_cirurgia for x in lipo_menos_1h):
                tempo -= 1
    if "Lipoaspiração" in nome_cirurgia:
        tempo += int(tempo_lipo - 1)
    return tempo, diaria
