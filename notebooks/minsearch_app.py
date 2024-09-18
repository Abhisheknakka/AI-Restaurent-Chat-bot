import streamlit as st
import time
from dotenv import load_dotenv
import os
from openai import OpenAI
from groq import Groq
import minsearch
import json
# Load environment variables
load_dotenv()

# Retrieve the API key from the environment
# Setup the OpenAI client to use either Groq, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")
API_HOST

if API_HOST == "groq":
    client = client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
    MODEL_NAME = os.getenv("GROQ_MODEL")

elif API_HOST == "ollama":
    client = openai.OpenAI(
        base_url=os.getenv("OLLAMA_ENDPOINT"),
        api_key="nokeyneeded",
    )
    MODEL_NAME = os.getenv("OLLAMA_MODEL")

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    MODEL_NAME = os.getenv("GITHUB_MODEL")

else:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL_NAME = os.getenv("OPENAI_MODEL")


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
        model=MODEL_NAME,
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
