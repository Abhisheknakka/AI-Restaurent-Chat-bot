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


# Setup the OpenAI client to use either Groq, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")
API_HOST

if API_HOST == "groq":
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
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


import ingest
index =ingest.load_index()


"""
def search(query):
    boost ={}

    results = index.search(
        query = query,
        filter_dict = {}
        boost_dict = boost,
        num_results = 10
    )
"""

def minsearch(query):
    return index.search(query)

def build_prompt(query, search_results):
    prompt_template = """You are a highly trained professional who have good knowledge on the menu and dishes present in the menu. Answer the questions which user asks based on the  CONTEXT from teh menu dataset. 
    Use only facts from the CONTEXT when answering the QUESTION. If the CONTEXT doesnt contain the amswer, output generic answer'
    QUESTION :{question}
    CONTEXT : {context}
    """.strip()
    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt
import asyncio


import asyncio

# Make llm an async function to be awaited
def llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# Modify rag function to call the async llm function using asyncio.run
def rag(query):
    search_results = minsearch(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)  # Direct call, no async handling
    return answer


