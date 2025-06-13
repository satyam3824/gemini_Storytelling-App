

import streamlit as st
import hmac

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

from google import genai

client = genai.Client(api_key= st.secrets["api_key"]["api_key"]) #API KEY

st.header("Story Telling Experience")
# main application starts
def story_telling(text):

    """
    A placeholder function for story telling.
    """
    if not text.strip():
        return "Please enter text."
    
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[f"Generate a creative story based on the given input from the user : {text}."]
)

    # This is where your actual logic would go.
    
    checked_text = f"{response.text}"
    
    return checked_text


st.title("Story Topic")
st.write("Type your text below and click 'Check' to get suggestions.")


user_input = st.text_area(
    "Your Text:",
    height=200,
    placeholder="Enter text here..."

)

if st.button("Check"):
    if user_input:
        result = story_telling(user_input)
        st.subheader("Result:")
        st.markdown(result)
    else:
        st.warning("Please enter some text.")

st.markdown("---")
st.caption("Story Telling")
