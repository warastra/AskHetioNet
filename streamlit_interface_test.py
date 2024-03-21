import streamlit as st
from streamlit.components.v1 import html
import requests, json

st.title('HetioNet QnA')
st.header('Ask a Biomedical Knowledge Graph!')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("Assistant"):
    conv_start = "Hello! how can i help?"
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
    url = 'http://127.0.0.1:8001/ask_hetionet'
    history_json = json.dumps(st.session_state.messages)
    # myobj = {'question': question, 'chat_history':history_json}

    st.chat_message("User").markdown(question)
    st.session_state.messages.append({"role": "User", "content": question})
    
    # api_response = requests.post(url, json = myobj)
    with st.spinner('Processing..'):
        api_response = requests.get(url + f'?q={question}')
        result_json = api_response.json()
        response  = result_json['query_engine_response']
      
    # Display Assistant response in chat message container
    with st.chat_message("Assistant"):
        st.markdown(response)
    
    # Add Assistant response to chat history
    st.session_state.messages.append({"role": "Assistant", "content": response})  # sources is added here so that it can appear when streamlit reruns, ideally it should not be included because the message history is passed to LLM to generate history-modified question
    
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