import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os
import streamlit_authenticator as stauth
import qmod as qm


class CustomPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'BI' , size = 14)
        self.cell(0, 10, txt = "Dr. Thiago Jung Mendaçolli", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
        self.cell(0, 10, txt = "CIRURGIA PLÁSTICA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
        self.cell(0, 10, txt = ("_" * 60), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')

    def footer(self):
        self.set_y(-40)
        self.set_font("Helvetica", size = 10)
        self.cell(0, 10, txt = ("_" * 60), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
        self.multi_cell(0, 10, txt = "Clínica Bioethos: Rua Padre Montoya, 300 - Centro - CEP 85851-080, Foz do Iguaçu - PR\nTel: (45) 3028-1282 - Whats: (45) 98805-0334 www.drthiagocirurgiaplastica.com.br", align = 'C')

def save_pdf(pdf, patient_name, document_text, doc_type, document_date=None, include_date=False):
    pdf.set_auto_page_break(auto=True, margin=40)
    pdf.add_page()
    pdf.set_font("Helvetica", size = 12)
    if doc_type:
        pdf.cell(0, 20, txt = doc_type, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
    pdf.cell(0, 20, txt = f"Nome: {patient_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'L')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt = document_text)
    if include_date and document_date is not None:
        pdf.ln(30)
        pdf.cell(0, 10, txt = f"{document_date.strftime('%d/%m/%Y')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')


def main():
     # Create or get the session state
    if "session" not in st.session_state:
        st.session_state.session = qm.SessionState()
        
    if 'patient_name' not in st.session_state:
        st.session_state['patient_name'] = ''  
    
    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")
    
    st.title('Laudos Médicos')
    receitas_folder = "src/laudos"

    # list all .txt files in the 'src/receitas' directory
    document_type = sorted([os.path.splitext(f)[0] for f in os.listdir(receitas_folder) if f.endswith('.txt')])
    
    selected_file  = st.sidebar.selectbox(
        'Que tipo de documento você gostaria de criar?',
        document_type
    )
    
    # add the .txt extension back onto the selected file name
    selected_file_with_ext = selected_file + '.txt'
    # read the selected file and put its contents into the 'document_text' variable
    with open(os.path.join(receitas_folder, selected_file_with_ext), 'r', encoding="UTF-8") as file:
        document_text = file.read()
        
    patient_name = st.text_input('Nome do Paciente', value=st.session_state.patient_name, key="pacient_name")
    st.session_state.patient_name = patient_name
    doc_type = st.text_input('Tipo de Documento', value="")
    document_text = st.text_area('Texto do Documento', height=300, value=document_text)
    document_date = st.date_input('Data do Documento', value=None)
    include_date = st.checkbox('Incluir data no documento')

    colb1, colb2 = st.columns(2)
    if colb1.button('Criar Documento'):
        filename = "my_pdf.pdf"
        pdf = CustomPDF(orientation="P", unit="mm", format="A4")
        save_pdf(pdf, patient_name, document_text, doc_type, document_date, include_date)
        # Output the PDF
        pdf.output(filename)

        # Show the PDF
        qm.show_pdf(filename)

    # Download the PDF
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
    table_pass = st.secrets['table_pass']["pass"]
    
    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        main()
