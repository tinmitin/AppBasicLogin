import streamlit as st
import toml
from auth_utils import check_authentication  # Import authentication utility

# Load the secrets to manage user profiles
secrets = toml.load(".streamlit/secrets.toml")

def update_profile(username, new_name, new_password):
    """Update the user's profile information and save changes to the TOML file."""
    if username in secrets["profile"]:
        # Update the profile information in the internal dictionary
        secrets["profile"][username]["name"] = new_name
        secrets["profile"][username]["password"] = new_password

        # Update the passwords section to reflect the new password
        secrets["passwords"][username] = new_password

        # Save changes back to the TOML file
        with open(".streamlit/secrets.toml", "w") as toml_file:
            toml.dump(secrets, toml_file)

        st.success("Profile updated successfully!")

def main():
    check_authentication()  # Verify if the user is authenticated
    logged_user = st.session_state.get("logged_user", None)
    if not logged_user:
        st.warning("You need to log in first.")
        return

    st.title("Profile Page")
    st.write("Update your profile information below.")
    user_profile = secrets["profile"].get(logged_user, {})

    # Display current profile information in the input fields
    new_name = st.text_input("New Name", value=user_profile.get("name", ""))
    new_password = st.text_input("New Password", value=user_profile.get("password", ""), type="password")

    # Update profile when button is clicked
    if st.button("Update Profile"):
        update_profile(logged_user, new_name, new_password)

if __name__ == "__main__":
    main()
