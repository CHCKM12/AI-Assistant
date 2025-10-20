import os
import streamlit as st
# import your API calling code
import requests

# Load env vars
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def call_deepseek_api(prompt: str):
    endpoint = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-chat",
        "prompt": prompt,
        "max_tokens": 8192,
        "stream": False  # streaming is more complex in python/streamlit
    }
    resp = requests.post(endpoint, json=body, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # parse data according to API spec
    return data["choices"][0]["message"]["content"]

def main():
    st.title("Hex AI Assistant (Streamlit version)")

    st.sidebar.header("Configuration")
    # maybe inputs for payload type, recon data, etc.

    prompt = st.text_area("Enter your instruction/prompt for the assistant:")

    if st.button("Generate"):
        with st.spinner("Contacting AI…"):
            answer = call_deepseek_api(prompt)
        st.write("### Response:")
        st.write(answer)
        # Optionally log conversation to Supabase / store context

if __name__ == "__main__":
    main()
