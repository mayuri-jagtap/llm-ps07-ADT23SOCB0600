import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Page title
st.title("Research Paper Abstract Simplifier")
st.write("Enter a research abstract and your own instruction.")

# Research abstract input
abstract = st.text_area(
    "Research Abstract",
    height=250,
    placeholder="Paste your research abstract here..."
)

# User prompt input
prompt = st.text_area(
    "Your Prompt / Instruction",
    height=150,
    placeholder="Example: Explain this abstract in simple language for a first-year student."
)

# Generate button
if st.button("Generate Result"):

    # Check abstract
    if not abstract:
        st.warning("Please enter a research abstract.")

    # Check prompt
    elif not prompt:
        st.warning("Please enter a prompt or instruction.")

    # Generate response
    else:
        full_prompt = f"""
Research Abstract:
{abstract}

User Instruction:
{prompt}
"""

        try:
            # Show loading message
            with st.spinner("Generating response..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=full_prompt
                )

            # Display original and generated result side by side
            st.subheader("Original Abstract vs Generated Result")

            col1, col2 = st.columns(2)

            # Left column
            with col1:
                st.markdown("### Original Abstract")

                st.text_area(
                    "Original",
                    abstract,
                    height=350,
                    disabled=True,
                    label_visibility="collapsed"
                )

            # Right column
            with col2:
                st.markdown("### Generated Result")

                with st.container(border=True):
                    st.markdown(response.text)

        except Exception as e:
            st.error("Something went wrong while generating the response.")
            st.error(str(e))