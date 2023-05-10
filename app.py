import streamlit as st
from .llm_logics import convert_mail

st.set_page_config(
    page_title="TransMailApp",
    page_icon="💻",
    #layout="wide",
    #initial_sidebar_state="collapse",
)

st.title("TransMailApp")
st.markdown("Aplicación web para formalizar y traducir emails.")

#"st.session_state_object:", st.session_state

user_email = st.experimental_user["email"]
user_acount = st.experimental_user["email"].split("@")[0]
st.info(f"Bienvenido, {user_acount} !")

if st.session_state.get("email_input",None):
    st.caption("último mail enviado:")
    st.caption(st.session_state.email_input[:50]+"...")

st.header("Introduce un texto para formalizar y traducir")

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Escoge el idioma al que traducir",
        ("Inglés","Francés"),
        index=1,
    )

lang_map ={
    "Inglés" : "english",
    "Francés" : "french",    
}

language = lang_map[language]

with col2:
    opcion_llm = st.selectbox(
        "Escoge el modelo a emplear",
        ("openai",)
    )

temperature = st.slider("Escoger un valor de aleatoriedad",min_value=0.0,max_value=1.0,step=0.1,key="temp")

def contar_palabras():
    num_words = len(st.session_state["email_input"].split())
    st.session_state["num_words"] = num_words
    return num_words

def get_text():
    email = st.text_area(
        label="Email Input",
        label_visibility='collapsed',
        placeholder="Escribe aquí tu email...",
        key="email_input",
        on_change=contar_palabras)
    
    return email

email = get_text()

nwords = st.session_state.get("num_words",0)
st.caption(f"Palabras: {nwords}/700")

if len(email.split()) > 700:
    st.error("El email es demasiado largo.",icon="🛑")
    st.stop()

if email:
    with st.spinner("Pensando..."):
        response = convert_mail(language=language,email=email,llm_source=opcion_llm,temperatura=temperature)
    st.divider()
    st.subheader("Email respuesta:")
    st.write(response)