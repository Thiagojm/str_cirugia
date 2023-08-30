import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import modules.qmod as qm
import streamlit_authenticator as stauth
import os
from modules.cred_file import *
from modules.mongo_mod import *


class CustomPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'BI', size=15)
        self.cell(200, 10, txt=NAME,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.cell(200, 10, txt=ESPECIALIDADE,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.cell(0, 10, txt=("_" * 60), new_x=XPos.LMARGIN,
                  new_y=YPos.NEXT, align='C')

    def footer(self):
        self.set_y(-40)
        self.set_font("Helvetica", size=12)
        self.cell(0, 10, txt=("_" * 60), new_x=XPos.LMARGIN,
                  new_y=YPos.NEXT, align='C')
        self.multi_cell(0, 10, txt=FOOTER, align='C')


def save_pdf(pdf, patient_name, document_text, doc_type, document_date=None, include_date=False):
    pdf.set_auto_page_break(auto=True, margin=40)
    pdf.add_page()
    pdf.set_font("Helvetica", size=15)
    pdf.cell(0, 20, txt=doc_type, new_x=XPos.LMARGIN,
             new_y=YPos.NEXT, align='C')
    pdf.cell(0, 20, txt=f"Nome: {patient_name}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=document_text)
    if include_date and document_date is not None:
        pdf.ln(30)
        pdf.cell(0, 10, txt=f"{document_date.strftime('%d/%m/%Y')}",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')


def false_callback():
    for k in st.session_state.keys():
        if k.endswith("_labs") or k.endswith("_imagem") or k.endswith("_cardio") or k.endswith("_aval"):
            st.session_state[k] = False
        st.session_state["outr_ex"] = ""
        st.session_state["outros_img"] = ""
        st.session_state["outro_esp"] = ""
        st.session_state["obs_aval"] = "Solicito liberação pré-operatória."


def set_true(*lista):
    false_callback()
    for k in st.session_state.keys():
        if k in lista and k == "obs_aval":
            st.session_state[k] = "Solicito perda ponderal com meta de IMC < 28."

        elif k in lista:
            st.session_state[k] = True


def print_session():
    for k in st.session_state.keys():
        print(k, st.session_state[k])


def main():

    if 'patient_name' not in st.session_state:
        st.session_state['patient_name'] = ''

    if 'cirurgia_name' not in st.session_state:
        st.session_state['cirurgia_name'] = ''

    # Start Db
    # Create a connection using MongoClient
    client = init_connection()

    # Connect to the desired database
    db = client.drtjm

    # Lista padrão de exames
    lista_padrao = ["Hemograma Completo_labs", "TAP, TTPA_labs", "Eletrocardiograma com laudo_cardio", "Uréia e Creatinina_labs", "Glicemia_labs",
                    "Sódio e Potássio_labs", "Vitamina D_labs", "Beta-HCG_labs", "Anestesiologia (Whats/ Tel: 3576-8081)_aval", "Radiografia de Tórax PA + P_imagem"]

    # USG mama
    usg_mama = ["Ultrassonografia de Mamas (com classificação BIRADS)_imagem"]

    # USG Parede
    usg_parede = [
        "Ultrassonografia de Parede abdominal (para investigação de hérnias/ diástase)_imagem"]

    # Cardio
    cardio = ["Cardiologista_aval"]

    # Dermato + Endócrino
    end_nutri = ["Endocrinologista_aval", "Nutricionista_aval", "obs_aval"]

    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")

    st.title('Pré Operatório')

    patient_name = st.text_input(
        'Nome do Paciente', value=st.session_state.patient_name, key="pacient_name")
    st.session_state.patient_name = patient_name
    colt1, colt2, colt3, colt4, colt5 = st.columns(5)
    colt1.button("Padrão", on_click=set_true, args=lista_padrao)
    colt2.button("USG Mama", on_click=set_true, args=usg_mama)
    colt3.button("USG Parede", on_click=set_true, args=usg_parede)
    colt4.button("Cardio", on_click=set_true, args=cardio)
    colt5.button("End + Nutri", on_click=set_true, args=end_nutri)
    st.divider()

    st.header('Exames Laboratoriais')

    # Create two columns
    col1, col2 = st.columns(2)

    # Read the file and create a checkbox for each line, alternating between the two columns
    selections = {}  # Dictionary to store the selections
    content = get_document_content(db, "outros", "Labs")
    lines = content.splitlines()
    for i in range(len(lines)):
        # Remove the newline character at the end of the line
        line = lines[i]
        # Alternate between columns based on the index of the line
        if i % 2 == 0:
            selections[line] = col1.checkbox(line, key=line + "_labs")
        else:
            selections[line] = col2.checkbox(line, key=line + "_labs")

    # Add a text area for additional notes or input
    outros_exames = st.text_area("Exames Adicionais", "", key="outr_ex")
    st.divider()

    # Imagem
    st.header('Exames de Imagem')

    # Create two columns
    col2, col3 = st.columns(2)

    # Read the file and create a checkbox for each line, alternating between the two columns
    imagem_selections = {}  # Dictionary to store the selections
    content = get_document_content(db, "outros", "Imagem")
    lines = content.splitlines()
    for i in range(len(lines)):
        # Remove the newline character at the end of the line
        line = lines[i]
        # Alternate between columns based on the index of the line
        if i % 2 == 0:
            imagem_selections[line] = col2.checkbox(
                line, key=line + "_imagem")
        else:
            imagem_selections[line] = col3.checkbox(
                line, key=line + "_imagem")

    # Add a text area for additional notes or input
    outros_imagem = st.text_area("Exames Adicionais", "", key="outros_img")
    st.divider()

    st.header('Exames Cardiológicos')

    # Create two columns
    col4, col5 = st.columns(2)

    # Read the file and create a checkbox for each line, alternating between the two columns
    cardio_selections = {}  # Dictionary to store the selections
    content = get_document_content(db, "outros", "Cardio")
    lines = content.splitlines()
    for i in range(len(lines)):
        # Remove the newline character at the end of the line
        line = lines[i]
        # Alternate between columns based on the index of the line
        if i % 2 == 0:
            cardio_selections[line] = col4.checkbox(
                line, key=line + "_cardio")
        else:
            cardio_selections[line] = col5.checkbox(
                line, key=line + "_cardio")

    st.divider()
    st.header('Avaliação de Especialista')
    # Here you can add the elements you want to show under "Avaliação de Especialista"
    # Read the file and create a checkbox for each line, alternating between the two columns
    cirurgia_name = st.text_input(
        'Indicação', value=st.session_state.cirurgia_name, key="cirurgia_name")
    aval_selections = {}  # Dictionary to store the selections
    content = get_document_content(db, "outros", "Aval")
    lines = content.splitlines()
    for i in range(len(lines)):
        # Remove the newline character at the end of the line
        line = lines[i].strip()
        # Alternate between columns based on the index of the line
        aval_selections[line] = st.checkbox(line, key=line + "_aval")

    outro_esp = st.text_input("Outro", "", key="outro_esp")
    # Add a text area for additional notes or input
    obs_aval = st.text_area(
        "Observações", "Solicito liberação pré-operatória.", key="obs_aval")
    st.divider()

    document_date = st.date_input('Data do Documento', value=None, )
    include_date = st.checkbox('Incluir data no documento')

    st.divider()
    colb1, colb2, colb3 = st.columns(3)
    if colb1.button('Criar Documento'):
        # Generate document text for Exames Laboratoriais
        document_text_labs = ""
        for item, selected in selections.items():
            if selected:
                document_text_labs += "- " + item + "\n"
        document_text_labs += outros_exames

        # Generate document text for Exames de Imagem
        document_text_imagem = ""
        for item, selected in imagem_selections.items():
            if selected:
                document_text_imagem += "- " + item + "\n"
        document_text_imagem += outros_imagem

        # Generate document text for Exames de Imagem
        document_text_cardio = ""
        for item, selected in cardio_selections.items():
            if selected:
                document_text_cardio += "- " + item + "\n"

        # Generate document text for Avaliação de Especialista
        document_text_aval = ""
        if any(aval_selections.values()) or outro_esp:
            document_text_aval = f"INDICAÇÃO: {cirurgia_name}\n\nESPECIALIDADE:\n"
            for item, selected in aval_selections.items():
                if selected:
                    document_text_aval += "- " + item + "\n"
            if outro_esp:
                document_text_aval += f"- {outro_esp}\n"
            document_text_aval += f"\nOBSERVAÇÃO:\n{obs_aval}"

        # Replace these with the actual values you want to use
        filename = "my_pdf.pdf"
        doc_type_labs = "Exames Laboratoriais"
        doc_type_imagem = "Exames de Imagem"
        doc_type_cardio = "Exames Cardiológicos"
        doc_type_aval = "Avaliação de Especialista"

        # Create FPDF object
        pdf = CustomPDF(orientation="P", unit="mm", format="A4")

        # Save PDF for Exames Laboratoriais
        if document_text_labs:
            save_pdf(pdf, patient_name, document_text_labs,
                     doc_type_labs, document_date, include_date)
        # Save PDF for Exames de Imagem
        if document_text_imagem:
            save_pdf(pdf, patient_name, document_text_imagem,
                     doc_type_imagem, document_date, include_date)
        # Save PDF for Exames de Cardio
        if document_text_cardio:
            save_pdf(pdf, patient_name, document_text_cardio,
                     doc_type_cardio, document_date, include_date)
        # Save PDF for Aval
        if document_text_aval:
            save_pdf(pdf, patient_name, document_text_aval,
                     doc_type_aval, document_date, include_date)

        # Output the PDF
        pdf.output(filename)

        # Show the PDF
        qm.show_pdf(filename)

    # Download the PDF
    if os.access("my_pdf.pdf", os.R_OK):
        with open('my_pdf.pdf', "rb") as f:
            colb2.download_button('Download PDF', f, file_name="Documento.pdf")

    # Clear checkboxes
    colb3.button("Limpar", on_click=false_callback)


if __name__ == "__main__":
    # Create an instance of the Authenticate class
    authenticator = stauth.Authenticate(
        dict(st.secrets['credentials']),
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days'],
        st.secrets['preauthorized']
    )

    name, authentication_status, username = authenticator.login(
        "Login", "main")
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        main()
