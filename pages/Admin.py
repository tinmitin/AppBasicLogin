import streamlit as st
import toml
from auth_utils import check_authentication  # Import the authentication utility

# Load the secrets to manage user permissions
secrets = toml.load(".streamlit/secrets.toml")

# Define the available permissions based on what the app supports
AVAILABLE_PAGES = ["Home", "Info", "Customers", "Page 1", "Page 2", "Admin"]

def update_permissions(username, new_permissions, new_role):
    """Update the permissions and role for a user in the secrets dictionary."""
    secrets["permissions"][username] = new_permissions
    secrets["roles"][username] = new_role

    # Save changes back to the TOML file
    with open(".streamlit/secrets.toml", "w") as toml_file:
        toml.dump(secrets, toml_file)

    st.success(f"Permissions and role updated successfully for {username}!")

def update_user_status(username, active_status):
    """Activate or deactivate a user."""
    secrets["active_users"][username] = active_status

    with open(".streamlit/secrets.toml", "w") as toml_file:
        toml.dump(secrets, toml_file)

    status = "activated" if active_status else "deactivated"
    st.success(f"User {username} has been {status}!")

def main():
    check_authentication()  # Ensure the user is authenticated

    # Check if the logged-in user is an admin
    if st.session_state.get("user_role") != "admin":
        st.error("You don't have permission to access this page.")
        return

    st.title("Admin Page")
    st.write("Manage user permissions, roles, and status here.")

    # List all users and their permissions and roles
    for username in secrets["permissions"].keys():
        st.subheader(f"User: {username}")
        user_permissions = secrets["permissions"].get(username, [])
        user_role = secrets["roles"].get(username, "user")
        active_status = secrets["active_users"].get(username, True)

        st.write(f"Current Permissions: {user_permissions}")
        st.write(f"Current Role: **{user_role.capitalize()}**")
        st.write(f"Active Status: **{'Active' if active_status else 'Inactive'}**")

        # Filter out invalid permissions
        corrected_permissions = [perm for perm in user_permissions if perm in AVAILABLE_PAGES]

        # Allow admins to update permissions for each user
        new_permissions = st.multiselect(
            f"Select permissions for {username}",
            AVAILABLE_PAGES,  # List of available options
            default=corrected_permissions,  # Only include valid defaults
        )

        # Allow admins to change the role
        new_role = st.selectbox(f"Select role for {username}", ["user", "admin"], index=0 if user_role == "user" else 1)

        # Toggle active/inactive status
        new_status = st.checkbox(f"Active status for {username}", value=active_status)

        if st.button(f"Update {username}"):
            update_permissions(username, new_permissions, new_role)
            update_user_status(username, new_status)

    # Section to add a new user
    st.markdown("---")
    st.subheader("Create a New User")
    new_username = st.text_input("New Username")
    new_name = st.text_input("New User's Name")
    new_password = st.text_input("New Password", type="password")
    new_user_role = st.selectbox("Role for New User", ["user", "admin"])

    if st.button("Create New User"):
        if new_username and new_name and new_password:
            create_new_user(new_username, new_name, new_password, new_user_role)
        else:
            st.error("Please fill in all fields to create a new user.")

def create_new_user(username, name, password, role="user"):
    """Create a new user profile, permissions, and add to active users."""
    if username in secrets["passwords"]:
        st.warning(f"User '{username}' already exists. Choose a different username.")
        return

    # Create new user entry
    secrets["passwords"][username] = password
    secrets["profile"][username] = {"name": name, "password": password}
    secrets["roles"][username] = role
    secrets["permissions"][username] = ["Home"]  # Default permission
    secrets["active_users"][username] = True

    # Save changes back to the TOML file
    with open(".streamlit/secrets.toml", "w") as toml_file:
        toml.dump(secrets, toml_file)

    st.success(f"New user '{username}' created successfully!")

if __name__ == "__main__":
    main()
