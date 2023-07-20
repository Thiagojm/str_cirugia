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
        

def save_pdf(pdf, patient_name, document_text, doc_type, document_date=None, include_date=False):
    pdf.add_page()
    pdf.set_font("Helvetica", size = 15)
    pdf.cell(0, 20, txt = doc_type, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')
    pdf.cell(0, 20, txt = f"Nome: {patient_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'L')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt = document_text)
    if include_date and document_date is not None:
        pdf.ln(30)
        pdf.cell(0, 10, txt = f"{document_date.strftime('%d/%m/%Y')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align = 'C')


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title('Pré Operatório')
    
    patient_name = st.text_input('Nome do Paciente')
    st.divider()
    
    st.header('Exames Laboratoriais')

    # Create two columns
    col1, col2 = st.columns(2)

    # Read the file and create a checkbox for each line, alternating between the two columns
    selections = {}  # Dictionary to store the selections
    with open("scr/labs/Labs.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()  # Remove the newline character at the end of the line
            # Alternate between columns based on the index of the line
            if i % 2 == 0:
                selections[line] = col1.checkbox(line)
            else:
                selections[line] = col2.checkbox(line)

    # Add a text area for additional notes or input
    outros_exames = st.text_area("Exames Adicionais", "")
    st.divider()
    
    # Imagem
    st.header('Exames de Imagem')

    # Create two columns
    col2, col3 = st.columns(2)

    # Read the file and create a checkbox for each line, alternating between the two columns
    imagem_selections = {}  # Dictionary to store the selections
    with open("scr/imagem/imagem.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()  # Remove the newline character at the end of the line
            # Alternate between columns based on the index of the line
            if i % 2 == 0:
                imagem_selections[line] = col2.checkbox(line, key=line + "_imagem")
            else:
                imagem_selections[line] = col3.checkbox(line, key=line + "_imagem")

    # Add a text area for additional notes or input
    outros_imagem = st.text_area("Exames Adicionais", "", key="outros_imagem")
    st.divider()

    st.header('Exames Cardiológicos')
    # Here you can add the elements you want to show under "Exames Cardiológicos"

    st.header('Avaliação de Especialista')
    # Here you can add the elements you want to show under "Avaliação de Especialista"

    document_date = st.date_input('Data do Documento', value=None, )
    include_date = st.checkbox('Incluir data no documento')
    
    if st.button('Criar Documento'):
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

        # Replace these with the actual values you want to use
        filename = "my_pdf.pdf"
        doc_type_labs = "Exames Laboratoriais"
        doc_type_imagem = "Exames de Imagem"

        # Create FPDF object
        pdf = CustomPDF(orientation="P", unit="mm", format="A4")

        # Save PDF for Exames Laboratoriais
        save_pdf(pdf, patient_name, document_text_labs, doc_type_labs, document_date, include_date)
        # Save PDF for Exames de Imagem
        save_pdf(pdf, patient_name, document_text_imagem, doc_type_imagem, document_date, include_date)

        # Output the PDF
        pdf.output(filename)

        # Show the PDF
        show_pdf(filename)




if __name__ == "__main__":
    main()