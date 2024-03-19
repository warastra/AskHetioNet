import streamlit as st
# from llm_model import generate_answer_with_source
from streamlit.components.v1 import html
# from open_ai_agent_qa_conv import bm_ai
import requests, json

# st.title('Capres Pemilu QnA')
# st.header('Yuk Lebih Melek Politik!')
st.title('Iklim dan Sustainability QnA')
st.header('Yuk Lebih Melek Lingkungan!')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("Assistant"):
    conv_start = "Hello! Mau Tanya Apa Hari Ini?"
    st.markdown(conv_start)
    # st.session_state.messages.append({"role": "Assistant", "content": conv_start})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# question = st.chat_input("Say something")
# while True:
# for i in range(3):
if question := st.chat_input("Say something"):
    url = 'http://127.0.0.1:8080/thematic_search'
    history_json = json.dumps(st.session_state.messages)
    # myobj = {'question': question, 'chat_history':history_json}

    st.chat_message("User").markdown(question)
    st.session_state.messages.append({"role": "User", "content": question})
    
    # api_response = requests.post(url, json = myobj)
    with st.spinner('Processing..'):
        api_response = requests.get(url + f'?q={question}')
        result_json = api_response.json()
        response  = result_json['refined_answer']
        sources = result_json['sources']
        sources = 'Temukan informasi lebih lanjut di\n' + '\n\n'.join(sources)
      
    # Display Assistant response in chat message container
    with st.chat_message("Assistant"):
        st.markdown(response)
        st.markdown(sources)
    
    # Add Assistant response to chat history
    st.session_state.messages.append({"role": "Assistant", "content": response})  # sources is added here so that it can appear when streamlit reruns, ideally it should not be included because the message history is passed to LLM to generate history-modified question
    st.session_state.messages.append({"role": "Assistant", "content": sources})
    
css = '''
<style>
html, body, [class*="css"]  {
    font-family: 'Tangerine';
    }
section.main > div:has(~ footer ) {
    padding-right: 5px;
    padding-left: 5px;
}
</style>

'''
st.markdown(css, unsafe_allow_html=True)