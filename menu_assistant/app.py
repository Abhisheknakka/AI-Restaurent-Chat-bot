import streamlit as st
from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
import uuid  # For generating conversation IDs
from dotenv import load_dotenv
import os
from rag import rag  # Importing the rag function from your rag.py file

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Endpoint model for `/ask`
class AskRequest(BaseModel):
    question: str

# Endpoint model for `/feedback`
class FeedbackRequest(BaseModel):
    conversation_id: str
    feedback: int  # Can be either +1 or -1

# Create a dictionary to store conversation history
conversation_history = {}

# FastAPI route for handling question POST request
@app.post("/ask")
async def ask_question(req: AskRequest):
    question = req.question
    conversation_id = str(uuid.uuid4())  # Generate unique conversation ID
    
    # Call the rag function to get the answer
    answer = rag(question)

    # Store conversation history (you can store this in a database later)
    conversation_history[conversation_id] = {
        "question": question,
        "answer": answer
    }

    # Return the answer along with the conversation ID
    return {
        "conversation_id": conversation_id,
        "answer": answer
    }

# FastAPI route for handling feedback POST request
@app.post("/feedback")
async def give_feedback(req: FeedbackRequest):
    conversation_id = req.conversation_id
    feedback = req.feedback
    
    # For now, just acknowledge the feedback
    if conversation_id in conversation_history:
        # Process the feedback (for example, write to a database in the future)
        return {"status": "Feedback received", "conversation_id": conversation_id, "feedback": feedback}
    else:
        return {"error": "Conversation ID not found"}

# Streamlit UI
def main():
    st.image(r"D:\Projects\AI-Restaurent-Chat-bot\input_data\jack_menu\logo.jpg", width=500)

    st.title("Jacks Chat Application")

    user_input = st.text_input("Chatbot is ready to help with menu. Ask your questions:")

    if st.button("Ask"):
        with st.spinner('Processing...'):
            response = rag(user_input)  # Call rag function
            st.success("Completed!")
            st.write(response)

# Ensure that the FastAPI and Streamlit apps run correctly
if __name__ == "__main__":
    main()
