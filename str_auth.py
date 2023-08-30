import streamlit_authenticator as stauth


hashed_passwords = stauth.Hasher(["123", "123"]).generate()
print(hashed_passwords)
