from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader    ## read PDF files
from langchain.text_splitter import RecursiveCharacterTextSplitter ## split the text into smaller chunks
from langchain_google_genai import GoogleGenerativeAIEmbeddings    ##  for generating embeddings using Google AI
from langchain_community.vectorstores import FAISS    ## Facebook AI Similarity Search
from langchain_google_genai import ChatGoogleGenerativeAI   ## for chatting capabilities usinh Google GEN AI
from langchain.chains.question_answering import load_qa_chain    ## load the question-answering chain
from langchain.prompts import PromptTemplate    ## define the template for prompt
 
load_dotenv()
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
 
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
 
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks
 
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks,embedding=embeddings)
    vector_store.save_local("chatwithpdf/faiss_index")
 
st.set_page_config(page_title="Chat with PDF",page_icon="📜")
st.header("My Chat With PDF Web Application")
user_question = st.text_input("Ask a question from PDF...")
 
with st.sidebar:
    st.title("Menu")
    pdf_docs = st.file_uploader("Upload PDF files and click on the submit button to process",
                                accept_multiple_files=True,type=['pdf'])
    submit = st.button("Submit & Process")
    if submit:
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        st.success("Done")