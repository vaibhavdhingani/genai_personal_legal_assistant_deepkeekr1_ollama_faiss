from prompt import custom_prompt_template, document_review_promt
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

## Setup LLM (Using DeepSeek R1 with Groq)
llm_model=ChatGroq(model="deepseek-r1-distill-llama-70b")

## Retrive Docs
def retrieve_docs(faiss_db, query):
    return faiss_db.similarity_search(query)

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

## Answer
def answer_query(faiss_db, query, service_requested):
    documents = retrieve_docs(faiss_db, query)
    context = get_context(documents)
    
    if service_requested=="Legal Analysis" :
        prompt = ChatPromptTemplate.from_template(custom_prompt_template)
        chain = prompt | llm_model
        return chain.invoke({"question": query, "context": context})
    
    elif service_requested=="Document Review" :
        prompt = ChatPromptTemplate.from_template(document_review_promt)
        chain = prompt | llm_model
        return chain.invoke({"context": context})
        
    elif service_requested=="Legal Drafting" :
        return
    
    else:
        return

#question="If a government forbids the right to assemble peacefully which articles are violated and why?"
#retrieved_docs=retrieve_docs(question)
#print("AI Lawyer: ", answer_query(documents=retrieved_docs, model=llm_model, query=question))