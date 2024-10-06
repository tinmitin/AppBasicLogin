import streamlit as st
from auth_utils import check_authentication, check_permissions

def main():
    check_authentication()  # Verify if the user is authenticated
    check_permissions("Info", st.session_state.get("permissions", []))  # Check if the user has permission
    st.title("Info")
    st.write("This is the content of **Page 2**.")

if __name__ == "__main__":
    main()
