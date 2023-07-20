import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import base64
import os


class CustomPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'BI' , size = 15)
        self.cell(200, 10, txt = "Dr. Thiago Jung Mendaçolli", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
        self.cell(200, 10, txt = "CIRURGIA PLÁSTICA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
        self.cell(0, 10, txt = ("_" * 60), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')

    def footer(self):
        self.set_y(-40)
        self.set_font("Helvetica", size = 12)
        self.cell(0, 10, txt = ("_" * 60), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
        self.multi_cell(0, 10, txt = "Clínica Bioethos: Rua Padre Montoya, 300 - Centro - CEP 85851-080, Foz do Iguaçu - PR\nTel: (45) 3028-1282 - Whats: (45) 98805-0334 www.drthiagocirurgiaplastica.com.br", align = 'C')

def save_pdf(filename, patient_name, document_text, document_date=None, include_date=False):
    pdf = CustomPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=60)
    pdf.add_page()
    pdf.set_font("Helvetica", size = 15)
    pdf.cell(0, 20, txt = f"RECEITA MÉDICA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
    pdf.cell(0, 20, txt = f"Nome: {patient_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'L')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt = document_text)
    if include_date and document_date is not None:
        pdf.ln(30)
        pdf.cell(0, 10, txt = f"{document_date.strftime('%d/%m/%Y')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
    pdf.output(filename)

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title('Emissão de Documentos Médicos')
    receitas_folder = "scr/receitas"

    # list all .txt files in the 'src/receitas' directory
    document_type = [os.path.splitext(f)[0] for f in os.listdir(receitas_folder) if f.endswith('.txt')]
    
    selected_file  = st.sidebar.selectbox(
        'Que tipo de documento você gostaria de criar?',
        document_type
    )
    
    # add the .txt extension back onto the selected file name
    selected_file_with_ext = selected_file + '.txt'
    # read the selected file and put its contents into the 'document_text' variable
    with open(os.path.join(receitas_folder, selected_file_with_ext), 'r') as file:
        document_text = file.read()
        
    patient_name = st.text_input('Nome do Paciente')
    document_text = st.text_area('Texto do Documento', height=300, value=document_text)
    document_date = st.date_input('Data do Documento', value=None)
    include_date = st.checkbox('Incluir data no documento')

    if st.button('Criar Documento'):
        filename = "my_pdf.pdf"
        save_pdf(filename, patient_name, document_text, document_date, include_date)
        show_pdf(filename)

if __name__ == "__main__":
    main()
