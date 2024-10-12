import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os
import streamlit_authenticator as stauth
import modules.qmod as qm
import modules.template as tp
from modules.cred_file import *
from modules.mongo_mod import *


st.set_page_config(
    page_title="Termos",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto",
)


class CustomPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'BI', size=14)
        self.cell(0, 10, text=TERMO_NAME,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.cell(0, 8, text=TERMO_TXT,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.cell(0, 8, text=("_" * 60), new_x=XPos.LMARGIN,
                  new_y=YPos.NEXT, align='C')

    def footer(self):
        self.set_y(-30)
        self.set_font("Helvetica", size=8)
        self.cell(0, 6, text=("_" * 110), new_x=XPos.LMARGIN,
                  new_y=YPos.NEXT, align='C')
        self.multi_cell(0, 6, text=FOOTER, align='C')


def save_pdf(pdf, patient_name, document_text, cirurgia_name, observacao, termo_template, document_date=None, include_date=False):
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    if document_text:
        pdf.cell(0, 10, text=TERMO_TXT,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(5)
        pdf.multi_cell(0, 6, text=document_text)
        if observacao:
            pdf.ln(5)
            pdf.multi_cell(0, 6, text=f"Observações: {observacao}")
        pdf.add_page()
    termo_result = tp.change_template(
        patient_name, cirurgia_name, termo_template)
    pdf.ln(5)
    pdf.multi_cell(0, 5, text=termo_result)
    if include_date and document_date is not None:
        pdf.ln(30)
        pdf.cell(0, 10, text=f"{document_date.strftime('%d/%m/%Y')}",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')


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

    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")

    st.title('Termos de Consentimento')

    patient_name = st.text_input(
        'Nome do Paciente', value=st.session_state.patient_name, key="pacient_name")
    st.session_state.patient_name = patient_name

    # list all documents in the 'Atestados' collection
    termos_coll = "Termos"
    documents = list_field_names(db, termos_coll)

    selected_file = st.selectbox(
        'Selecione um template.',
        documents
    )

    # get value from document
    doc_value = get_document_content(db, termos_coll, selected_file)

    cirurgia_name = st.text_input(
        'Qual Cirurgia?', value=st.session_state.cirurgia_name, key="cir_name")
    st.session_state.cirurgia_name = cirurgia_name
    observacao = st.text_area('Observações', value="")
    document_text = st.text_area(
        'Texto do Documento', height=300, value=doc_value)
    document_date = None
    include_date = None

    colb1, colb2 = st.columns(2)
    if colb1.button('Criar Documento'):
        filename = "my_pdf.pdf"
        cirurgia_formated = f"{cirurgia_name.upper()},"
        pdf = CustomPDF(orientation="P", unit="mm", format="A4")
        termo_template = get_document_content(db, "outros", "Termo Geral")
        save_pdf(pdf, patient_name, document_text, cirurgia_formated,
                 observacao, termo_template, document_date, include_date)
        # Output the PDF
        pdf.output(filename)

        # Show the PDF
        qm.show_pdf(filename)

    # Download the PDF
    if os.access("my_pdf.pdf", os.R_OK):
        with open('my_pdf.pdf', "rb") as f:
            colb2.download_button('Download PDF', f, file_name="Documento.pdf")


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
