import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from modules.qmod import show_pdf_2


st.set_page_config(
    page_title="TUSS",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
)


def main():
    authenticator.logout("Logout", "sidebar")

    st.title('Excel Sheet Viewer')

    uploaded_file = "src/AMB TUSS ORDENADA.xlsx"

    if uploaded_file:
        try:
            xls = pd.ExcelFile(uploaded_file, engine='openpyxl')
            sheet_names = xls.sheet_names
            selected_sheet = st.selectbox("Select a sheet", sheet_names)

            if selected_sheet:
                df = pd.read_excel(
                    uploaded_file, selected_sheet, engine='openpyxl')
                df = df.astype(str)
                st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.write("Error reading file:", e)

    st.divider()

    if st.button("Tabela Completa"):
        filename = "src/TABELA TUSS.pdf"
        show_pdf_2(filename)


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
