import streamlit as st
import streamlit_authenticator as stauth


def main():

    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")

    st.title('Cálculo de Imposto')

    with st.container():
        col1, col2 = st.columns(2)
        valor_nota = col1.text_input("Valor da Nota", value="0")
        col2.markdown('##')
        btn1 = col2.button("Calcular")
        try:
            valor_bruto = float(valor_nota.replace(",", "."))
        except Exception as e:
            st.toast(f"Valor inválido, {e}", icon="❗")
            st.warning(f"Valor inválido, {e}", icon="❗")
            return
        if btn1:
            st.toast(
                'Sucesso', icon="✔️")
    st.divider()

    with st.container():
        if valor_bruto:
            data_1 = {
                'Valor Bruto': str(valor_bruto).replace(".", ","),
                "PIS (0,65%)": str(round((valor_bruto * 0.0065), 2)).replace(".", ","),
                "COFINS (3%)": str(round((valor_bruto * 0.03), 2)).replace(".", ","),
                "IR (1,5%)": str(round((valor_bruto * 0.015), 2)).replace(".", ","),
                "CSLL (1%)": str(round((valor_bruto * 0.01), 2)).replace(".", ","),
                "Total Líquido": str(round((valor_bruto - (valor_bruto * 0.0615)), 2)).replace(".", ","),
            }

            data_2 = {
                'Imposto de 15,33%': str(round((valor_bruto * 0.1533), 2)).replace(".", ","),
                "Total - 15,33%": str(round((valor_bruto * 0.8467), 2)).replace(".", ","),
                "Transferir p/ Inter": str(round((valor_bruto * 0.0918), 2)).replace(".", ","),
                "IR HMIF (4,8%)": str(round((valor_bruto * 0.048), 2)).replace(".", ","),

            }

            col3, col4 = st.columns(2)
            # Convert dictionary to table format
            table_data_1 = {"Imposto": list(
                data_1.keys()), "": list(data_1.values())}
            table_data_2 = {"Outros": list(
                data_2.keys()), "": list(data_2.values())}

            # Fica dando warning
            col3.dataframe(table_data_1, hide_index=True,
                           use_container_width=True)
            col4.dataframe(table_data_2, hide_index=True,
                           use_container_width=True)

    st.divider()

    with st.container():
        col5, col6 = st.columns(2)
        col5.markdown("BMF CPL SERVICOS DE SAUDE LTDA: 25254480000148")

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
