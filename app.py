
import streamlit as st
import requests
import html

st.set_page_config(page_title="AI Language Translator", page_icon="🌍")

st.title("🌍 AI Language Translator")
st.write("Translate text between different languages.")

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Urdu": "ur",
    "French": "fr"
}

text = st.text_area("Enter your text:")

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox("Translate from:", languages.keys())

with col2:
    target = st.selectbox("Translate to:", languages.keys())

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter some text.")
    elif source == target:
        st.warning("Choose different languages.")
    else:
        try:
            with st.spinner("Translating..."):
                response = requests.get(
                    "https://api.mymemory.translated.net/get",
                    params={
                        "q": text,
                        "langpair": f"{languages[source]}|{languages[target]}"
                    },
                    timeout=30
                )

                response.raise_for_status()
                data = response.json()

                if data.get("responseStatus") == 200:
                    result = html.unescape(
                        data["responseData"]["translatedText"]
                    )
                    st.success("Translation")
                    st.write(result)
                else:
                    st.error("Translation service could not translate this text.")

        except requests.RequestException:
            st.error("Connection problem. Please check your internet.")
