import streamlit as st
from backend import *
# import os
# from dotenv import load_dotenv
# load_dotenv()
# openai.api_key = os.getenv("API_KEY")

def main():
    # df=pd.read_csv('processed/vn_embeddings.csv', index_col=0)
    df=pd.read_csv(INPUT_FILE, index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)



    st.write('## Q&A Bot')
    prompt = st.text_input(label='label', placeholder='Ai là CEO của Cohost AI?', label_visibility='hidden')
    if st.button(label='Send'):
        answer = answer_question(question=prompt,df = df, debug=True)
        st.write(answer)


if __name__ == '__main__':
    main()