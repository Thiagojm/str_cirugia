import os
import json
import streamlit as st
import streamlit_authenticator as stauth
import math
import qmod as qm


def main():
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
    authenticator.logout("Logout", "sidebar")
    sorted_dates = sorted(options, key=lambda x: (x.split('/')[1], x.split('/')[0]), reverse=True)
    selected_tabela = st.sidebar.selectbox("Escolha uma tabela de preço:", sorted_dates)

    # Carrega o arquivo .json correspondente à tabela selecionada
    if selected_tabela:
        with open(os.path.join(data_dir, json_files[options.index(selected_tabela)]), "r", encoding='utf-8') as json_file:
            data_tabela = json.load(json_file)
            

    ####### Pagina principal #######

    ####### IMC #######

    # Header
    st.header("Calculadora Dr. Thiago Jung")
    st.divider()
    # Cria duas colunas
    col1, col2 = st.columns(2)

    # Cria campos para o usuário inserir sua altura e peso na primeira coluna
    with col1:
        altura_cm = st.text_input("Insira sua altura (em cm):", value=170)
        peso = st.text_input("Insira seu peso (em kg):", value=70.0)

    # Converte a altura do usuário de centímetros para metros
    altura_cm = float(altura_cm)
    peso = float(peso.replace(",", "."))
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
        st.write(f"Para um IMC de 28, o peso seria: {peso_imc_28:.2f} kg")
        st.write(f"Para um IMC de 30, o peso seria: {peso_imc_30:.2f} kg")

    st.divider()
    ####### Cirurgias #######
    st.subheader("Cirurgias")
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

    st.divider()
    tipo_protese = st.selectbox("Escolha uma Textura", ["Texturizada", "Poliuretano"])
    st.divider()
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
        if checked_boxes:
            msg = qm.calculate(checked_boxes, extra_values, data_tabela)
            conversation.append({"message": msg})
            # Display the conversation
            message = ""
            for entry in conversation:
                message += entry["message"]
            st.divider()
            st.text_area(" ", value=message, height=800, max_chars=10000)

            # Update the session state
            st.session_state.session.messages = conversation
        else:
            st.info('Selecione pelo menos uma cirurgia', icon="ℹ️")
    
if __name__ == "__main__":
    # Create an instance of the Authenticate class
    authenticator = stauth.Authenticate(
    dict(st.secrets['credentials']),
    st.secrets['cookie']['name'],
    st.secrets['cookie']['key'],
    st.secrets['cookie']['expiry_days'],
    st.secrets['preauthorized']
)

    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        main()
    
