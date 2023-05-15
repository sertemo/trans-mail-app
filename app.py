import streamlit as st
import llm_logics as lg

st.set_page_config(
    page_title="TransMailApp",
    page_icon="💻",
    #layout="wide",
    #initial_sidebar_state="collapse",
)


st.title("TransMailApp  📧")
st.markdown("Aplicación web para formalizar y traducir :red[emails].")

"st.session_state_object:", st.session_state


st.info(f"Bienvenid@ !")
col1, col2 = st.columns(2)

with col1:
    if st.session_state.get("last_response"):
        if st.checkbox("Ver última respuesta"):        
            st.markdown("Última respuesta recibida:")
            st.markdown(st.session_state.last_response[:150]+"...")

with col2:
    if st.session_state.get("contador"):
        st.write("Número de generaciones:",st.session_state.contador)

st.header("Introduce un texto para formalizar y traducir")

col3, col4 = st.columns(2)

with col3:
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

with col4:
    opcion_llm = st.selectbox(
        "Escoge el modelo a emplear",
        ("openai",)
    )

temperature = st.slider("Escoge un valor de creatividad",min_value=0.0,max_value=1.0,step=0.1,key="temp")

def contar_palabras(texto:str=""):
    num_words = len(texto.split())
    return num_words

@st.cache_data
def get_response(texto:str,language:str)->str:
    response = lg.convert_mail(
        language=language,
        email=texto,
        llm_source=opcion_llm,
        temperatura=temperature)
    return response

def contar_generaciones():
    if st.session_state.get("contador"):
        if st.session_state["contador"] < 3:
            st.session_state["contador"] += 1
        else:
            st.error("Has alcanzado el límite de consultas por sesión.")
            st.stop()
    else:
        st.session_state["contador"] = 1

email = st.text_area(
        label="Email Input",
        label_visibility='collapsed',
        placeholder="Escribe aquí tu email...",
        key="email_input",
        on_change=contar_generaciones)

nwords = contar_palabras(email)
st.caption(f"Palabras: {nwords}/700")

if len(email.split()) > 700:
    st.error("El email es demasiado largo.",icon="🛑")
    st.stop()

if st.button("Generar respuesta"):
    if email:        
        st.divider()
        st.subheader("Email respuesta:")
        response = get_response(email,language)
        st.write(response)
        st.session_state["last_response"] = response