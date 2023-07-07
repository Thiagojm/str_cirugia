import os
import json
import streamlit as st
import math

# Define o caminho para o diretório "data"
data_dir = "data"

# Lista os arquivos no diretório "data"
files = os.listdir(data_dir)

######### Menu Suspenso #########

# Cria uma lista vazia para armazenar as opções do menu suspenso
options = []

# Itera sobre cada arquivo no diretório "data"
for f in files:
    # Verifica se o arquivo tem a extensão ".json"
    if f.endswith(".json"):
        # Define o caminho completo para o arquivo
        file_path = os.path.join(data_dir, f)
        
        # Abre o arquivo e carrega o conteúdo como um dicionário
        with open(file_path, "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
            
            # Verifica se a chave "DATA_DA_TABELA" está presente no dicionário
            if "DATA_DA_TABELA" in data:
                # Adiciona o valor associado à chave "DATA_DA_TABELA" à lista de opções
                options.append(data["DATA_DA_TABELA"])

# Inverte a ordem das opções na lista
options.reverse()

# Cria o menu suspenso na barra lateral com as opções
selected_option = st.sidebar.selectbox("Escolha uma tabela de preço:", options)

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
col1, col2 = st.columns(2)

# Cria um dicionário vazio para armazenar o status de cada checkbox
checkbox_status = {}

# Itera sobre cada arquivo no diretório "data"
for f in files:
    # Verifica se o arquivo tem a extensão ".json"
    if f.endswith(".json"):
        # Define o caminho completo para o arquivo
        file_path = os.path.join(data_dir, f)
        
        # Abre o arquivo e carrega o conteúdo como um dicionário
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            
            # Verifica se a chave "DATA_DA_TABELA" está presente no dicionário e corresponde à opção selecionada pelo usuário
            if "DATA_DA_TABELA" in data and data["DATA_DA_TABELA"] == selected_option:
                # Verifica se a chave "CIRURGIAS_EQUIPE" está presente no dicionário
                if "CIRURGIAS_EQUIPE" in data:
                    # Ordena os valores na lista associada à chave "CIRURGIAS_EQUIPE" em ordem alfabética
                    sorted_values = sorted(data["CIRURGIAS_EQUIPE"])
                    
                    # Calcula o número de valores em cada coluna
                    values_per_column = math.ceil(len(sorted_values) / 2)
                    
                    # Itera sobre cada valor na lista ordenada
                    for i, value in enumerate(sorted_values):
                        # Verifica se o índice é menor que o número de valores por coluna
                        if i < values_per_column:
                            # Cria um checkbox na primeira coluna e associa seu status a uma variável no dicionário checkbox_status
                            checkbox_status[value] = col1.checkbox(value)
                        else:
                            # Cria um checkbox na segunda coluna e associa seu status a uma variável no dicionário checkbox_status
                            checkbox_status[value] = col2.checkbox(value)

# Cria um menu suspenso expansível com o título "Extras"
with st.expander("Extras"):
    # Cria campos de entrada para os valores especificados
    valor_ajuste = st.number_input("Valor de Ajuste:", min_value=0.0, step=0.01)
    valor_protese = st.number_input("Valor da Prótese:", min_value=0.0, step=0.01)
    tempo_lipo = st.number_input("Tempo de Lipo (h):", min_value=0.0, step=0.01)
    tempo_sala = st.number_input("Tempo de Sala (h):", min_value=0.0, step=0.01)
    dias_internamento = st.number_input("Dias de internamento:", min_value=0, step=1)
    valor_anestesia = st.number_input("Valor Anestesia:", min_value=0.0, step=0.01)
    valor_equipe = st.number_input("Valor Equipe:", min_value=0.0, step=0.01)
    
for key, value in checkbox_status.items():
    if value:
        st.markdown(f"<span style='color: blue'>{key}</span>", unsafe_allow_html=True)