from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate
from langchain import OpenAI
from typing import Literal
import os


#OPENAI_API_KEY = st.secrets.api_keys["OPENAI_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

template = """
    Below is an email that may be poorly worded.
    This email is written in spanish.
    Your goal is to:
    - Translate the input text to a specified language.
    - Convert the input text to a very formal tone.
    - Deliver the response in an email format.
    
    Below is the email,  and language:
    LANGUAGE: {language}
    EMAIL: {email}
    
    YOUR RESPONSE:
"""
""" #Definimos el modelo
llm_hug = HuggingFaceHub(
    #repo_id="google/flan-t5-xxl",
    model_kwargs={
        "temperature":0.5,
        "max_length":512},
        huggingfacehub_api_token=HUGGINGFACE_API_KEY
) """

prompt = PromptTemplate(
    input_variables=["language","email"],
    template=template
)

def convert_mail(
        language:Literal["french","english"],
        email:str,
        temperatura:float,
        llm_source:Literal["openai","huggingface"]="openai",
        )->str:
    
    """ Dados un email, un llm y un idioma, devuelve el mismo email,\n
    en lenguaje formal y traducido al idioma seleccionado
     
    Parameters
    ----------
    *language* : idioma para traducir el email

    *email* : El email a formatear y traducir

    *llm* : el modelo que se usará para la traducción: 'openai' o 'huggingface'
    Actualmente el modelo de huggingface no funciona.
     """
    #Definimos modelo OpenAI
    llm_open = OpenAI(
    model_name="text-davinci-003",
    temperature=temperatura,
    openai_api_key=OPENAI_API_KEY
    )

    llm = llm_open if llm_source == "openai" else None
    format_prompt = prompt.format(language=language,email=email)
    #print(f"Prompt que se enviará a la API del modelo {llm.__class__.__name__}:\n{format_prompt}")
    return llm(format_prompt)

if __name__ == '__main__':
    pass
