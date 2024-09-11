from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model for storing conversations
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    question = Column(Text)
    answer = Column(Text)

Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app initialization
app = FastAPI()


# Endpoint model for `/ask`
class AskRequest(BaseModel):
    question: str

# Endpoint model for `/feedback`
class FeedbackRequest(BaseModel):
    conversation_id: str
    feedback: int  # Can be either +1 or -1

from pydantic import BaseModel
import uuid

class AskRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    conversation_id: str
    feedback: int  # Can be either +1 or -1

# Create a dictionary to store conversation history (for testing purposes)
conversation_history = {}

@app.post("/ask")
async def ask_question(req: AskRequest, db: Session = Depends(get_db)):
    question = req.question
    conversation_id = str(uuid.uuid4())  # Generate unique conversation ID

    # Call the rag function to get the answer
    answer = rag(question)

    # Store conversation history in database
    db.add(Conversation(conversation_id=conversation_id, question=question, answer=answer))
    db.commit()

    return {
        "conversation_id": conversation_id,
        "answer": answer
    }

@app.post("/feedback")
async def give_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    conversation_id = req.conversation_id
    feedback = req.feedback

    # Process the feedback
    conversation = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
    if conversation:
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
