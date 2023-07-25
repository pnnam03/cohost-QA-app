import pandas as pd
import os
import re

domain = 'en.cohost.vn'
output_file_name = 'processed/en_scraped.csv'


def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('..', '.')
    return serie

# Create a list to store the text files
to_returns=[]

# Get all the text files in the text directory
for file in os.listdir("text/" + domain + "/"):

    # Open the file and read the text
    with open("text/" + domain + "/" + file, "r", encoding="UTF-8") as f:
        texts = f.readlines()
        texts = [text[:-1].strip().strip('.') for text in texts if text != "\n"]
        # print(file, texts, len(texts))
        texts = texts[18:-22]
        to_returns += texts

# Create a dataframe from the list of texts
df = pd.DataFrame(to_returns, columns = ['text'])
df.to_csv(output_file_name)


