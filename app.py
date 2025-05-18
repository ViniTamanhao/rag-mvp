import streamlit as st
import requests

API_URL = "https://greenplatypus.club/query" 

st.title("🔍 Query with LLM & Retrieved Context")

# -- API Key Handling (in-memory only) --
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key_input = st.text_input(
    "Enter your API key", value=st.session_state.api_key, type="password"
)
if st.button("Save API Key"):
    st.session_state.api_key = api_key_input
    st.success("API Key stored in session!")

# -- Query Input --
query = st.text_area("Write your query:", height=150)

if st.button("Send Query"):
    if not st.session_state.api_key or not query.strip():
        st.error("Please provide both an API key and a query.")
    else:
        try:
            response = requests.post(
                API_URL,
                headers={"api-key": st.session_state.api_key},
                json={"query": query},
            )
            response.raise_for_status()
            result = response.json()

            st.subheader("🧠 LLM Answer")
            st.write(result.get("answer", "No answer returned."))

            st.subheader("📚 Retrieved Context")
            st.write(result.get("context", "No context returned."))

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
