# Import necessary libraries
import json
import pandas as pd
import openai
import elasticsearch
from groq import Groq
from dotenv import load_dotenv
import os
from sklearn.feature_extraction.text import CountVectorizer
from tqdm.auto import tqdm
import minsearch


# Load environment variables
load_dotenv()

# Setup project paths
base_folder = 'D:/Projects/AI-Restaurent-Chat-bot/'
input_data_folder = base_folder + 'input_data/'


def load_index():

    with open(input_data_folder + 'food_user_qa_dataset.json', 'rt') as f_in:
        data = json.load(f_in)

    documents = []
    for dish in data['dishes']:
        dish_name = dish['dish name']
        for doc in dish['documents']:
            doc['dish_name'] = dish_name  # Add dish_name to each document
            documents.append(doc)

    index = minsearch.Index(
    text_fields = ['id', 'question','section','text','dish_name'],
    keyword_fields=['dish_name']
    #keyword_fields=['id']
    )

    index.fit(documents)
    return index


