import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-key-123")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///history.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Hugging Face model for detection
    DETECTOR_MODEL = "Hello-SimpleAI/chatgpt-detector-roberta" 
    # GPT-2 for Perplexity calculation
    PPL_MODEL = "gpt2"