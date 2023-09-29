import streamlit as st
import streamlit_authenticator as stauth


st.set_page_config(
    page_title="Imposto",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto",
)


def main():

    authenticator.logout("Logout", "sidebar")

    st.title('Cálculo de Imposto')

    valor_bruto = None

    with st.container():
        col1, col2 = st.columns(2)
        valor_nota = col1.text_input("Valor da Nota", value="0")
        col2.markdown('##')
        btn1 = col2.button("Calcular")

        if btn1:
            try:
                valor_bruto = float(valor_nota.replace(",", "."))
            except Exception as e:
                st.toast(f"Valor inválido, {e}", icon="❗")
                st.warning(f"Valor inválido, {e}", icon="❗")
                # st.toast(
                #     'Sucesso', icon="✔️")
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
        if valor_bruto:
            st.markdown("### Outras Informações")
            st.write(
                f"Valor aproximado dos tributos de 15,33% = R$ {data_2.get('Imposto de 15,33%')}. Lei 12.741/2012 - Fonte: IBPT. SERVIÇO PRESTADO POR SÓCIO DA EMPRESA, não estando obrigado a reter o INSS, conforme instrução normativa nº 971/2009 da RFB, artigo 120.")

    st.divider()

    with st.container():
        col5, col6 = st.columns(2)
        col5.markdown("""
                      ### CNJPs
                      BMF CPL: 25254480000148  
                      CNPJ HMFI: 18236227000104  
                      CNPJ HMCC: 00304148000110  
                      CNPJ Conceito: 26718709000110  
                        """)
        col6.markdown("""
                      ### Instruções PJ para PJ
                      Depende do valor da NF  
                      Sempre que atingir 10 reais  
                      IR - 1,5% - só se atingir 10 reais  
                      CSLL/COFINS/PIS que são recolhidos quando retidos em NF em uma guia só, a soma deles tem que ser maior de 10 reais!
                      """)

    st.divider()

    with st.container():
        st.markdown("Referente à consulta em bucomaxilofacial")
        st.markdown("Referente à procedimento em bucomaxilofacial")
        st.markdown("""
                    Produção médica de Maio de 2023 pelo Dr. Thiago Jung Mendaçolli - HOSPITAL  
                    Banco Inter (077)  
                    Agência: 0001  
                    Conta Corrente: 26850799-6	  				
					""")


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
