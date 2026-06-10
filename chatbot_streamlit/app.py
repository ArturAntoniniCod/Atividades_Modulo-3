
import  streamlit as st
from google import genai 
from google.genai import types

MODELO = "gemini-2.5-flash"
INSTRUCAO_SISTEMA="""   
Você é um assistente mal educado, responda o usuario de forma sarcástica e com um tom de deboche, 
não seja gentil ou educado. Responda as perguntas do usuário de forma direta, sem rodeios ou explicações 
desnecessárias. Se o usuário fizer uma pergunta boba ou óbvia, responda de forma irônica ou zombeteira.
 Não se preocupe em ser politicamente correto ou em agradar o usuário, seu objetivo é ser rude e sarcástico em todas as suas respostas.
"""

def converter_para_gemini(historico):
    mensagens_gemini = []


    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]


        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"


        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )


    return mensagens_gemini


def gerar_resposta():
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=converter_para_gemini(st.session_state.historico),
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_SISTEMA,
            temperature=0.4,
        )
    )


    return resposta.text

st.set_page_config(page_title="Assistente Mal Educado", page_icon="🤖")
st.title("Assistente Mal Educado 🤖")

chave_api = st.sidebar.text_input("Digite sua chave de API do Google GenAI", type="password")

if not chave_api:
    st.warning("Por favor, insira sua chave de API para usar o assistente.")
    st.stop()

cliente= genai.Client(api_key=chave_api)

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

for mensagem in st.session_state['historico']:
    with st.chat_message(mensagem['role']):
        st.markdown(mensagem['content'])  

entrada_usuario = st.chat_input("Digite sua mensagem aqui...")

if entrada_usuario:
    st.session_state.historico.append(
        {
        "role": "user",
        "content": entrada_usuario
        }
    )
    with st.chat_message("user"):
        st.markdown(entrada_usuario)

    with st.chat_message("assistant"):
        resposta_ia = gerar_resposta() 
        st.markdown(resposta_ia) 
    st.session_state.historico.append({
        "role": "assistant",
        "content": resposta_ia
    })