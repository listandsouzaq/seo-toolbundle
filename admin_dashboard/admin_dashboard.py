import streamlit as st
import hashlib

# Configuration for the admin panel
ADMIN_USER = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("574112".encode()).hexdigest()

def check_password():
    """Returns `True` if the user is logged in, `False` otherwise."""
    # Check if the user is already logged in
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # If not logged in, display the login form
    if not st.session_state["password_correct"]:
        st.subheader("Admin Login")
        with st.form("login_form"):
            st.text_input("Username", value=ADMIN_USER, disabled=True)
            password = st.text_input("Password", type="password", key="password_input")
            submitted = st.form_submit_button("Login")

            if submitted:
                # Check if the entered password matches the stored hash
                if hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                    st.session_state["password_correct"] = True
                    st.success("Login successful!")
                    st.rerun() # Use st.rerun() instead of st.experimental_rerun()
                else:
                    st.error("😕 Wrong password. Please try again.")
        return False
    else:
        return True

def main():
    """Main function for the admin dashboard."""
    st.set_page_config(
        page_title="Admin Dashboard",
        layout="wide"
    )

    if check_password():
        st.title("Admin Dashboard (Hidden)")
        st.info("Welcome to the secure back-end control panel.")
        
        # ======================================================================
        # BACK-END CONTROL PANEL FUNCTIONALITY
        # This section demonstrates how you can add administrative functions.
        # We will use st.session_state to manage a list of 'tools' dynamically.
        # ======================================================================
        
        st.subheader("Tool Management")
        st.write("Add, view, or remove tools from your application.")

        # Initialize a list of tools in session state if it doesn't exist
        if 'managed_tools' not in st.session_state:
            st.session_state['managed_tools'] = [
                {"name": "Example Tool 1", "description": "This is a pre-existing tool."},
                {"name": "Example Tool 2", "description": "Another example tool."}
            ]

        # Form to add a new tool
        with st.form("add_tool_form", clear_on_submit=True):
            st.subheader("Add a New Tool")
            new_tool_name = st.text_input("Tool Name")
            new_tool_description = st.text_area("Tool Description")
            add_button = st.form_submit_button("Add Tool")

            if add_button and new_tool_name and new_tool_description:
                new_tool = {"name": new_tool_name, "description": new_tool_description}
                st.session_state['managed_tools'].append(new_tool)
                st.success(f"Tool '{new_tool_name}' added successfully!")
                st.rerun()

        st.markdown("---")

        # Display and manage the list of tools
        st.subheader("Current Tools")
        if st.session_state['managed_tools']:
            for i, tool in enumerate(st.session_state['managed_tools']):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{tool['name']}**")
                    st.markdown(f"*{tool['description']}*")
                with col2:
                    if st.button("Remove", key=f"remove_tool_{i}"):
                        st.session_state['managed_tools'].pop(i)
                        st.success(f"Tool '{tool['name']}' removed.")
                        st.rerun()
        else:
            st.info("No tools have been added yet.")

if __name__ == "__main__":
    main()
