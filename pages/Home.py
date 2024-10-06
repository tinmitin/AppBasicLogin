import streamlit as st
from auth_utils import check_authentication  # Import authentication utility

def main():
    check_authentication()  # Verify if the user is authenticated
    st.title("Home Page")
    st.write("Welcome to the Home Page of your Streamlit app!")

if __name__ == "__main__":
    main()
