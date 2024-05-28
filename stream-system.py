import streamlit as st
from pptx import Presentation
import requests
from io import BytesIO

# Load presentation from URL
def load_presentation(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        pptx_file = BytesIO(response.content)
        return Presentation(pptx_file)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download presentation: {e}")
    except Exception as e:
        st.error(f"Failed to load presentation: {e}")

# Function to display the presentation
def display_presentation(presentation):
    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                st.write(shape.text)
            if shape.shape_type == 13:  # Checking if shape is a picture
                image = shape.image
                with st.container():
                    st.image(image.blob)

# Apply custom CSS to change the background color and make font bold
st.markdown(
    """
    <style>
    .main {
        background-color: #656D4E;
        color: white;  /* Optional: Set text color to white for better contrast */
    }
    .main * {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Credentials
USERNAME = "Gaza"
PASSWORD = "123"

# Main function to run the app
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        pptx_url = "https://github.com/MohammedHamza0/ML-App/raw/main/System%20Overview%20(1).pptx"
        presentation = load_presentation(pptx_url)
        if presentation:
            display_presentation(presentation)

# Login function
def login():
    st.title("Login Page") 
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state['logged_in'] = True
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()
