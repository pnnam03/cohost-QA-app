import tiktoken
import pandas as pd
import openai
import numpy as np
import time
import os
from dotenv import load_dotenv

##### CONST
MAX_TOKENS = 200
INPUT_FILE = 'processed/vn_scraped.csv'
OUTPUT_FILE = 'processed/vn_embeddings_200_200_100.csv'


openai.api_key = os.getenv("API_KEY")

#####


def count_token(string: str):
    # return len(tokenizer.encode(string))

    cleaned_string = string.strip()
    words_list = cleaned_string.split()

    return len(words_list)


# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv(INPUT_FILE, index_col=0)
df.columns = ['text']

# Tokenize the text and save the number of tokens to a new column
# df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
df['n_tokens'] = df.text.apply(lambda x: count_token(x))
# Function to split the text into chunks of a maximum number of tokens

def get(min_tokens: int, dir: int, chunk):
    # if dir == -1:
    #     chunk = reversed(chunk)
    
    tokens_so_far = 0
    returns = []
    if dir == 1:
        for x in chunk:
            tokens_so_far += x['n_tokens']
            returns.append(x)

            if tokens_so_far > min_tokens:
                break
    else:
        cnt_tokens = 0
        
        for x in reversed(chunk): 
            tokens_so_far += x['n_tokens']
            returns.append(x)

            if tokens_so_far > min_tokens:
                returns = list(reversed(returns))
                break

    return returns
    
def split_into_many(text):

    lines = text.split('||')
    
    n_tokens = [count_token(line) for line in lines]
    
    chunks = []
    chunk = []
    tokens_so_far = 0

    # Loop through the sentences and tokens joined together in a tuple
    for line, token in zip(lines, n_tokens):
        if line == "":
            continue
        chunk.append({
            'line' : line,
            'n_tokens' : token,
            })
        tokens_so_far += token

        if tokens_so_far > MAX_TOKENS:
            chunks.append(chunk)
            # print(tokens_so_far)
            chunk = []
            tokens_so_far = 0

    if tokens_so_far > 0:   
        chunks.append(chunk)

    returns = []
    for i,c in enumerate(chunks):
        from_prev_chunk, from_next_chunk = [], []
        if i > 0:
            if i+1 == len(chunks):
                from_prev_chunk = get(min_tokens= 200, dir = -1, chunk = chunks[i-1])
            else:
                from_prev_chunk = get(min_tokens= 100, dir = -1, chunk = chunks[i-1])

        if i+1 < len(chunks):
            if i == 0:
                from_next_chunk = get(min_tokens= 200, dir = +1, chunk = chunks[i+1])
            else:
                from_next_chunk = get(min_tokens= 100, dir = +1, chunk = chunks[i+1])
            
        cc = from_prev_chunk + c + from_next_chunk
        tmp = ""
        for x in cc:
            tmp += x['line']+'. '
        tmp.strip()

        # print(count_token(tmp), len(tmp.split()))
        # print(tmp+'\n')
        returns.append(tmp)

    return returns


shortened = []

# Loop through the dataframe
texts = ""
for row in df.iterrows():

    # If the text is None, go to the next row
    if row[1]['text'] is None:
        continue
    texts += row[1]['text']+'||'

shortened += split_into_many(texts)

x = 0
for i, s in enumerate(shortened):
    # print(i, count_token(s))
    x = max([x, count_token(s)])

print('number of embeddings = ',len(shortened),'\nmax(words_per_embeddin)g = ', x)

df = pd.DataFrame(shortened, columns = ['text'])
df['n_tokens'] = df.text.apply(lambda x: count_token(x))

embeddings = []
# calculate embeddings openai api

for i,text in enumerate(df['text']):
        tries = 0
        delay = 21
        while True:
            try:
                embedding = openai.Embedding.create(input=text, engine='text-embedding-ada-002')['data'][0]['embedding']
                embeddings.append(embedding)
                break
            except Exception as e:
                print(f'    ',e)
                print(f'    Failed at {tries}-th try')
                time.sleep(delay)
                tries += 1
        print(len(embeddings), '-th text: OK')  
        
df['embeddings'] = embeddings
# save embeddings to file
df.to_csv(OUTPUT_FILE)
