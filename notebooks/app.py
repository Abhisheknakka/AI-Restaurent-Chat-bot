import streamlit as st
import time
from dotenv import load_dotenv
import os

from elasticsearch import Elasticsearch
from openai import OpenAI


# Load environment variables
load_dotenv()

# Retrieve the API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
es_client = Elasticsearch('http://localhost:9200') 


def elastic_search(query):

    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "category": "menu items"  # Filter by category
                    }
                }
            }
        }
    }

    # Perform the search
    response = es.search(index=index_name, body=search_query)

    result_doc =[]

    for hit in response['hits']['hits']:
        result_doc = hit['_source']
        print(f"Section: {doc['section']}")
        print(f"Question: {doc['question']}")
        print(f"Answer: {doc['text']}")
        print("\n")

    return result_doc


def elastic_search(query, index_name = "menu-items"):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs

def build_prompt(query, search_results):
    prompt_template = """You are a highly trained professional who have good knowledge on the menu. Answer the questions which user asks based on the  CONTEXT from teh menu dataset. 
    Use only factsfrom the CONTEXT when answering the QUESTION. If the CONTEXT doesnt contain the amswer, output generic answer'
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
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(query):
    search_results = elastic_search(query)
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