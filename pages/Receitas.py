import streamlit as st
from fpdf import FPDF
import base64


class CustomPDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', size = 15)
        self.cell(200, 10, txt = "Dr. Thiago Jung Mendaçolli", ln = True, align = 'C')
        self.cell(200, 10, txt = "CIRURGIA PLÁSTICA", ln = True, align = 'C')
        self.cell(200, 10, txt = "MEMBRO DA S.B.C.P.", ln = True, align = 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-60)
        self.set_font("Arial", size = 12)
        self.multi_cell(0, 10, txt = "Clínica Bioethos: Rua Padre Montoya, 300 - Centro - CEP 85851-080, Foz do Iguaçu - PR\nTel: (45) 3028-1282 - Whats: (45) 98805-0334 www.drthiagocirurgiaplastica.com.br")

def save_pdf(filename, patient_name, document_text, document_date=None, include_date=False):
    pdf = CustomPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = f"Nome: {patient_name}", ln = True, align = 'L')
    pdf.ln(20)
    pdf.multi_cell(0, 10, txt = document_text)
    if include_date and document_date is not None:
        pdf.ln(40)
        pdf.cell(200, 10, txt = f"Data: {document_date.strftime('%d/%m/%Y')}", ln = True, align = 'L')
    pdf.output(filename)

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title('Emissão de Documentos Médicos')

    document_type = st.sidebar.selectbox(
        'Que tipo de documento você gostaria de criar?',
        ('Receita médica', 'Solicitação de exames', 'Atestado')
    )

    patient_name = st.text_input('Nome do Paciente')
    document_text = st.text_area('Texto do Documento', height=300)
    document_date = st.date_input('Data do Documento', value=None)
    include_date = st.checkbox('Incluir data no documento')

    if st.button('Criar Documento'):
        filename = "my_pdf.pdf"
        save_pdf(filename, patient_name, document_text, document_date, include_date)
        show_pdf(filename)

if __name__ == "__main__":
    main()
