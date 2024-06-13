import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import data_process as dp
import os 

st.set_page_config(layout='wide')

def main():
    # load_dotenv()
    # st.write (os.getlogin())
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
   
    st.title(':orange[Translation using OpenAI] :page_facing_up')

    # user_question = st.text_input("**Ask a question about your :blue[documents]:**")
    # if user_question:
    #     handle_userinput(user_question)

    # you can create columns to better manage the flow of your page
    # this command makes 2 columns of equal width
    col1, col2 = st.columns(2)

    with col1:
        logtxtbox = st.empty()
        logtxt = ''
        logtxtbox.text_area("Original Text: ",logtxt, height = 500)

    with col2:
        translated_txt_box = st.empty()
        translated_txt = ''
        translated_txt_box.text_area("Translation: ",translated_txt, height = 500)

    
    with st.sidebar:
        option = st.selectbox("Target Language:", ("English", "French", "Chinese"))

        st.subheader(":orange[Your documents]")

        uploaded_file = st.file_uploader(":blue[Upload File]"
                                     ,type=['txt','docx','pdf']
                                     ,accept_multiple_files=False)
        
        if st.button("Process Document"):
            # if uploaded_file:
            if uploaded_file is not None:
                file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
                # st.write(file_details)
                with st.spinner("Processing your document(s)"):
                    
                    raw_text = dp.extract_text(uploaded_file)
                    text_chunks = dp.chunk_text(raw_text)
                    counter = 0
                    for txt in text_chunks:
                        counter += 1
                        logtxt += txt + '\n'
                        with col1:
                            logtxtbox.text_area("Original: ", logtxt, height=500)

                        txt1 = dp.translate_text(txt, option)
                        
                        translated_txt += txt1 + '\n' #'****Counter [' + str(counter) + '] \n' +
                        
                        with col2:
                            translated_txt_box.text_area("Translation:", translated_txt, height=500)

                    # create conversation chain
                    # st.session_state.conversation = mp.get_chain(vectorstore)
                            
if __name__ == '__main__':
    main()