import streamlit as st
import streamlit_authenticator as stauth
from modules.qmod import show_pdf_2
import os



st.set_page_config(
    page_title="Internação",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
)


def main():

    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")

    st.title('Guia de Internação')
    filename = "src/Internacao.pdf"
    show_pdf_2(filename)

    st.divider()
    
    st.markdown("### Guia SADT")
    # Download the PDF
    sadt_path = "src/SADT.pdf"
    if os.access(sadt_path, os.R_OK):
        with open(sadt_path, "rb") as f:
            st.download_button('Download SADT', f, file_name="SADT_ITAMED.pdf")

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
