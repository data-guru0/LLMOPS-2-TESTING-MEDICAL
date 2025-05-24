# import streamlit as st
# from app.components.retriever import create_qa_chain

# from dotenv import load_dotenv

# load_dotenv()

# def main():
#     st.title("🔍 AI Medical Chatbot")
    
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         st.chat_message(message['role']).markdown(message['content'])

#     prompt = st.chat_input("Ask a medical question...")

#     if prompt:
#         st.chat_message('user').markdown(prompt)
#         st.session_state.messages.append({'role': 'user', 'content': prompt})

#         try:
#             qa_chain = create_qa_chain()
#             response = qa_chain.invoke({'query': prompt})

#             result = response["result"] 
#             st.chat_message('assistant').markdown(result)  
#             st.session_state.messages.append({'role': 'assistant', 'content': result})

#         except Exception as e:
#             st.error(f"Error: {str(e)}")

# if __name__ == "__main__":
#     main()