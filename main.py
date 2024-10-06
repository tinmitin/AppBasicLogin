import hmac
import streamlit as st
import toml
import os
import importlib.util

# Load and parse secrets to allow modifications
secrets = toml.load(".streamlit/secrets.toml")

def check_password():
    """Returns `True` if the user has the correct password and is active."""
    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state["username"]
        if (
            username in secrets["passwords"]
            and hmac.compare_digest(st.session_state["password"], secrets["passwords"][username])
            and secrets["active_users"].get(username, False)  # Check if the user is active
        ):
            st.session_state["password_correct"] = True
            st.session_state["logged_user"] = username
            st.session_state["user_role"] = secrets["roles"].get(username, "user")
            st.session_state["permissions"] = secrets["permissions"].get(username, ["Home"])  # Get permissions
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password if not logged in
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known, password incorrect, or user is deactivated.")
    return False

def logout():
    """Handle the logout functionality."""
    st.session_state.clear()  # Clear session state variables
    st.experimental_set_query_params()  # Reset the query parameters to clear URL state

# Check if user is logged in; if not, stop and show the login form
if not check_password():
    st.stop()

# At this point, the user is successfully logged in, so construct the sidebar
logged_user = st.session_state["logged_user"]
user_permissions = st.session_state["permissions"]

# Sidebar construction should only happen after successful login
if st.session_state.get("password_correct", False):
    # Create the sidebar for the authenticated user
    st.sidebar.title(f"Welcome, {secrets['profile'][logged_user]['name']}")
    selected_page = st.sidebar.selectbox("Select a page", user_permissions)
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        logout()

# Define the folder where pages are stored
pages_folder = "pages"

def load_page(page_name):
    """Dynamically load a page module from the pages folder."""
    formatted_page_name = page_name.replace(" ", "_")  # Convert "Page 1" to "Page_1"
    page_file = os.path.join(pages_folder, f"{formatted_page_name}.py")
    if os.path.exists(page_file):
        # Dynamically import the module using importlib
        spec = importlib.util.spec_from_file_location(page_name, page_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            module.main()  # Execute the main function of the module
        else:
            st.error(f"Page {page_name} does not have a `main()` function defined.")
    else:
        st.error(f"Page {page_name}.py not found in {pages_folder} directory.")

# Load the selected page only if a page is selected after login and permissions are loaded
if "selected_page" in locals():
    # Display the selected page content if a page is selected
    st.empty()  # Placeholder until the user selects a page
    if selected_page:  # Load only if a page is selected
        load_page(selected_page)
