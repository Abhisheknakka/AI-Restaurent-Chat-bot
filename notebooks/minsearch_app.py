import streamlit as st
import time
from dotenv import load_dotenv
import os
from openai import OpenAI
import minsearch
import json
# Load environment variables
load_dotenv()

# Retrieve the API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


base_folder = 'D:/Projects/AI-Restaurent-Chat-bot/'
input_data_folder = base_folder+'input_data/'

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
    )

index.fit(documents)

def minsearch(query):
    return index.search(query)


prompt_template = """

"""
def build_prompt(query, search_results):
    prompt_template = """
    You are a highly trained professional and helpful assistant that answers questions about food based off a menu data set.
    You must use the data set to answer the questions, you should not provide any info that is not in the provided sources.
    Answer the questions which user asks based on the  CONTEXT.
    Use only facts from the CONTEXT when answering the QUESTION.
    QUESTION :{question}
    CONTEXT : {context}
    """.strip()
    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def llm(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
            
            ]
    )

    """

    # test this
    response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": USER_MESSAGE + "\nSources: " + matches_table},
    ],)
    """
    
    return response.choices[0].message.content

def rag(query):
    search_results = minsearch(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer


def main():

    st.image(r"D:\Projects\AI-Restaurent-Chat-bot\input_data\jack_menu\logo.jpg", width=500)

    st.title("Jacks Chat Application") 

    user_input = st.text_input("Chatbot is ready to help with menu. Ask your questions:")

    if st.button("Ask"):
        with st.spinner('Processing...'):
            output = rag(user_input)
            st.success("Completed!")
            st.write(output)

if __name__ == "__main__":
    main()
