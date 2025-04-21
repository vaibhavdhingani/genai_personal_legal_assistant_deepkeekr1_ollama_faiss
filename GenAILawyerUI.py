import streamlit as st
from laywerResponse_rag_pipeline import answer_query
from learnDocument_vector_database import create_vector_store
import re

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebarHeader"]{
        visibility: hidden;
    }
    [data-testid="stElementToolbar"]{
        visibility: hidden;
    }
    [data-testid="stImageContainer"]{
        margin-top: -50px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
st.sidebar.image('Lawyer.jpg', use_container_width=True)

service_requested = st.sidebar.selectbox(
    "Services offered :",
    ("Document Review", "Legal Drafting", "Legal Analysis"),
    index=None,
    placeholder="Select service",
)
st.sidebar.markdown("<p><br></p>", unsafe_allow_html=True)

if service_requested=="Legal Analysis" :
    
    uploaded_file = st.sidebar.file_uploader("Upload Document", type="pdf", accept_multiple_files=False)
    filename = "placeholder"

    user_query = st.sidebar.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")
    ask_question = st.sidebar.button("Ask A Lawyer", type="primary", use_container_width=True)

    if ask_question:
        if uploaded_file and user_query:
            if(uploaded_file.name != filename) : 
                faiss_db = create_vector_store(uploaded_file)
                filename = uploaded_file.name

            response=answer_query(faiss_db, query=user_query, service_requested=service_requested)
            st.chat_message("user").write(user_query)
            st.chat_message("AI Personal Lawyer").write(re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL).strip())
    
        else :
            st.error("Kindly upload a valid PDF file and/or ask a valid Question!")


elif service_requested=="Document Review" :
    
    uploaded_file = st.sidebar.file_uploader("Upload Document", type="pdf", accept_multiple_files=False)   
    ask_question = st.sidebar.button("Ask A Lawyer", type="primary", use_container_width=True)

    if ask_question:
    
        if uploaded_file:
            faiss_db = create_vector_store(uploaded_file)
            response=answer_query(faiss_db, query="", service_requested=service_requested)
            st.markdown(re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL).strip())
    
        else :
            st.error("Kindly upload a valid PDF file !") 

elif service_requested=="Legal Drafting" :
  st.sidebar.write("Service uner development")


else:
  print("Please select service")