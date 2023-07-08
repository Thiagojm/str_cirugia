import os
import json
import streamlit as st
import math
import qmod as qm

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
            return
        if "Lipoescultura(2,5h)" in nome_cirurgia:
            if tempo_lipo == 0:
                tempo_lipo = 2.5
        elif "Lipoescultura(3h)" in nome_cirurgia:
            if tempo_lipo == 0:
                tempo_lipo = 3.5
        elif "Lipoaspiração" in nome_cirurgia and tempo_lipo == 0:
            st.warning("Escolha o tempo de lipoaspiração")
            return
        if "Mamoplastia com Prótese" in nome_cirurgia or "Prótese de Mama" in nome_cirurgia:
            tipo_protese = extras[7]
            if valor_protese == 0:
                valor_protese = int(data["PROTESES"][tipo_protese])
        ajuste_q = extras[0]
        tempo, diaria = qm.tempo_diaria(
            nome_cirurgia, data["CIRURGIAS_EQUIPE"], data["LIPO_MENOS_1H"], tempo_lipo
        )
        if extras[3] != "0":
            tempo = int(extras[3])
        if extras[4]:
            diaria = int(extras[4])
        valor_equipe_cirurgia = qm.valor_equipe(
            nome_cirurgia, data["CIRURGIAS_EQUIPE"], ajuste_q, tempo_lipo
        )
        valor_anestesista_foz = qm.valor_anestesia_foz(
            nome_cirurgia, tempo_lipo, data["ANESTESIA_FOZ"]
        )
        valor_anestesia_renata = qm.valor_anestesia_renata(
            nome_cirurgia, data["ANESTESIA_RENATA"], data["RENATA_CONS_MENOS"])

        if extras[5] != "0":
            valor_anestesista_foz = int(extras[5])
            valor_anestesia_renata = int(extras[5])

        if extras[6] != "0":
            valor_equipe_cirurgia = int(extras[6])
        
        valor_hosp_hmcc = qm.valor_hmcc(tempo, diaria, data["HMCC"])
        valor_hosp_unimed = qm.valor_unimed(tempo, diaria, data["UNIMED"])
        valor_hosp_hmd = qm.valor_hmd(tempo, diaria, data["HMD"])
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
        message = " \n".join([message, f"Valor da anestesia HMD: {valor_anestesia_renata} "])
        if valor_protese != 0:
            valor_total_hmcc += valor_protese
            valor_total_unimed += valor_protese
            valor_total_hmd += valor_protese
            message = " \n".join([message, f"Valor da prótese {tipo_protese}: {valor_protese} "])
        if tempo_lipo > 0:
            message = " \n".join([message, f"Tempo de Lipo: {tempo_lipo} horas "])
        message = " \n".join([message, f"Valor do hospitalar HMD: {valor_hosp_hmd} "])    
        message = " \n".join([message, f"Valor do hospitalar Unimed: {valor_hosp_unimed} "])
        message = " \n".join([message, f"Valor do hospitalar HMCC: {valor_hosp_hmcc} "])
        message = " \n".join([message, f"Valor total HMD: {valor_total_hmd} "])
        message = " \n".join([message, f"Valor total Unimed: {valor_total_unimed} "])
        message = " \n".join([message, f"Valor total HMCC: {valor_total_hmcc} "])
        message = " \n".join([message, "\n" + "#" * 29 + "\n" ])
        return message
    except Exception as e:
        st.error(f"Prencha todos os campos ou deixe em '0'.\nErro: {e}")
        print(e)

# Define o caminho para o diretório "data"
data_dir = "data"

# Lista os arquivos no diretório "data"
files = os.listdir(data_dir)

######### Menu Suspenso #########

# Cria uma lista vazia para armazenar as opções do menu suspenso
options = []

# Cria uma lista vazia para armazenar os nomes dos arquivos .json
json_files = []

# Itera sobre cada arquivo no diretório "data"
for f in files:
    # Verifica se o arquivo tem a extensão ".json"
    if f.endswith(".json"):
        # Adiciona o nome do arquivo à lista de arquivos .json
        json_files.append(f)
        
        # Define o caminho completo para o arquivo
        file_path = os.path.join(data_dir, f)
        
        # Abre o arquivo e carrega o conteúdo como um dicionário
        with open(file_path, "r", encoding='utf-8') as json_file:
            data = json.load(json_file)            
            options.append(data["DATA_DA_TABELA"])

# Define a class to handle session state
class SessionState:
    def __init__(self):
        self.messages = []

# Create or get the session state
if "session" not in st.session_state:
    st.session_state.session = SessionState()

# Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
sorted_dates = sorted(options, key=lambda x: (x.split('/')[1], x.split('/')[0]), reverse=True)
selected_tabela = st.sidebar.selectbox("Escolha uma tabela de preço:", sorted_dates)

# Carrega o arquivo .json correspondente à tabela selecionada
if selected_tabela:
    with open(os.path.join(data_dir, json_files[options.index(selected_tabela)]), "r", encoding='utf-8') as json_file:
        data_tabela = json.load(json_file)
        

####### Pagina principal #######

####### IMC #######

# Cria duas colunas
col1, col2 = st.columns(2)

# Cria campos para o usuário inserir sua altura e peso na primeira coluna
with col1:
    altura_cm = st.number_input("Insira sua altura (em cm):", min_value=0, value=170, step=1)
    peso = st.number_input("Insira seu peso (em kg):", min_value=0.0, value=70.0, step=0.1)

# Converte a altura do usuário de centímetros para metros
altura = altura_cm / 100

# Calcula o IMC
imc = peso / (altura * altura)

# Mostra o IMC do usuário na segunda coluna
with col2:
    st.write(f"Seu IMC é: {imc:.2f}")

    # Calcula os pesos correspondentes aos IMCs 28 e 30 para a altura do usuário
    peso_imc_28 = 28 * (altura * altura)
    peso_imc_30 = 30 * (altura * altura)

    # Mostra os pesos correspondentes aos IMCs 28 e 30 para a altura do usuário
    st.write(f"Para um IMC de 28 com sua altura, seu peso deveria ser: {peso_imc_28:.2f} kg")
    st.write(f"Para um IMC de 30 com sua altura, seu peso deveria ser: {peso_imc_30:.2f} kg")


####### Cirurgias #######
    
# Cria duas colunas
col3, col4 = st.columns(2)

# Cria um dicionário vazio para armazenar o status de cada checkbox
checkbox_status = {}


# Verifica se a chave "CIRURGIAS_EQUIPE" está presente no dicionário
if "CIRURGIAS_EQUIPE" in data_tabela:
    # Ordena os valores na lista associada à chave "CIRURGIAS_EQUIPE" em ordem alfabética
    sorted_values = sorted(data_tabela["CIRURGIAS_EQUIPE"])
    
    # Calcula o número de valores em cada coluna
    values_per_column = math.ceil(len(sorted_values) / 2)
    
    # Itera sobre cada valor na lista ordenada
    for i, value in enumerate(sorted_values):
        # Verifica se o índice é menor que o número de valores por coluna
        if i < values_per_column:
            # Cria um checkbox na primeira coluna e associa seu status a uma variável no dicionário checkbox_status
            checkbox_status[value] = col3.checkbox(value)
        else:
            # Cria um checkbox na segunda coluna e associa seu status a uma variável no dicionário checkbox_status
            checkbox_status[value] = col4.checkbox(value)

tipo_protese = st.selectbox("Escolha uma Textura", ["Texturizada", "Poliuretano"])

# Cria um menu suspenso expansível com o título "Extras"
with st.expander("Extras"):
    # Cria campos de entrada para os valores especificados
    valor_ajuste = st.text_input("Valor de Ajuste:", value="0")
    valor_protese = st.text_input("Valor da Prótese:", value="0")
    tempo_lipo = st.text_input("Tempo de Lipo (h):", value="0")
    tempo_sala = st.text_input("Tempo de Sala (h):", value="0")
    dias_internamento = st.text_input("Dias de internamento:", value="")
    valor_anestesia = st.text_input("Valor Anestesia:", value="0")
    valor_equipe = st.text_input("Valor Equipe:", value="0")

# Conversation
conversation = st.session_state.session.messages
    
# Cria um botão "Calcular"
if st.button("Calcular"):
    # Cria uma lista vazia para armazenar os nomes dos checkboxes marcados
    checked_boxes = []
    
    # Itera sobre cada item no dicionário checkbox_status
    for key, value in checkbox_status.items():
        # Verifica se o checkbox está marcado
        if value:
            # Adiciona o nome do checkbox à lista checked_boxes
            checked_boxes.append(key)
            
    # Cria uma lista para armazenar os valores dos campos extras
    extra_values = [valor_ajuste, valor_protese, tempo_lipo, tempo_sala, dias_internamento, valor_anestesia, valor_equipe, tipo_protese]
    
    # Chama a função calculate quando o botão for clicado
    msg = calculate(checked_boxes, extra_values, data_tabela)
    
    conversation.append({"user": "User", "message": msg})
    
# Display the conversation
message = ""
for entry in conversation:
    message += entry["message"]
st.text_area(" ", value=message, height=800, max_chars=10000)
        #st.write(f"{message}")

# Update the session state
st.session_state.session.messages = conversation