import streamlit as st

def check_authentication():
    """Check if the user is authenticated."""
    if not st.session_state.get("password_correct", False):
        st.warning("You need to log in first!")
        st.stop()

def get_logged_user_info(secrets):
    """Get the currently logged-in user's profile information."""
    username = st.session_state.get("logged_user")
    if username and username in secrets["profile"]:
        return secrets["profile"][username]
    return {}

def check_permissions(page_name, user_permissions):
    """Check if the user has permissions for the selected page."""
    if page_name not in user_permissions:
        st.error(f"You do not have permission to access {page_name}.")
        st.stop()
