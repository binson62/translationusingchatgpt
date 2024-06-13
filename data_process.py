import docx2txt
from PyPDF2 import PdfReader 
# PdfFileReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai

import streamlit as st
# import fitz
# import pdfplumber

# import docx

def extract_text(uploaded_file):
    raw_text = ''
    if uploaded_file.type == "text/plain":
        # raw_text = docx_file.read() # read as bytes
        # st.text(raw_text) # fails
        # st.text(str(docx_file.read(),"utf-8")) # empty
        raw_text = str(uploaded_file.read(),"utf-8") # works with st.text and st.write,used for futher processing
        # st.text(raw_text) # Works
        # st.write(raw_text) # works
	# elif uploaded_file.type == "application/pdf":
            
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raw_text = docx2txt.process(uploaded_file) # Parse in the uploadFile Class directory                          
    if uploaded_file.type == "application/pdf":
        textList = []
        # this works:
        pdfReader = PdfReader(uploaded_file)
        for page in pdfReader.pages:
            textList.append (page.extract_text())
        
        # with pdfplumber.open(uploaded_file) as pdf:
        #     for page in pdf.pages:
        #        textList.append (page.extract_text())
        raw_text = '\n'.join(textList)

        # thid does not work and gave error
        # doc = fitz.open(uploaded_file)  
        # textList = []
        # for page in doc:
        #     textList.append (page.get_text())
        #     raw_text = '\n'.join(textList)
    return raw_text


def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 0,
    length_function = len)

    texts = text_splitter.split_text(text)

    return texts


openai.api_key = st.secrets["openai_apikey"]

# Function to translate text using OpenAI
def translate_text(text, target_language='Chinese'):
  completion = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": f"Please translater the following text into {target_language}: {text}"
        },
    ])
  return completion.choices[0].message.content 