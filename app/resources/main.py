import streamlit as st
from router import router
from faq import ingest_faq_data ,faq_chain
from pathlib import Path


faqs_path=Path(__file__).parent /"faq_data.csv"

ingest_faq_data(faqs_path)

def ask(query):
    route= router(query).name
    if route=='faq':
        return faq_chain(query)
    else:
        return f"Route {route} not implemented yes"
    
st.title("E commerce chatbot")

query=st.chat_input("Write your query") ## it will create chat gpt like input box

if "messages"  not in st.session_state:
    st.session_state["messages"]=[] ##### it is usede to previous state of conversation

for message  in st.session_state.messages:
    with st.chat_message(message['role']): ##### this will show  role  icon in the UI interface
        st.markdown(message['content'])

if query:
    with st.chat_message("user"):### chat message is used to show you message
        st.markdown(query)
    st.session_state.messages.append({"role":"user","content":query}) ## this the default of messages that llm consume

    respone=ask(query)
    with st.chat_message("assistant"):### as we used assistant so it will show robot icon on the chat
        st.markdown(respone)
    st.session_state.messages.append({"role":"assistant","content":respone})