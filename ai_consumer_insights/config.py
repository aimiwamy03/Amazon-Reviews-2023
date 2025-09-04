"""
Configuration settings for AI Consumer Insights Platform
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Model Settings
    SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "gpt-3.5-turbo"  # Using 3.5 for cost efficiency
    
    # Data Settings
    SAMPLE_SIZE = 1000  # For demo purposes
    MAX_REVIEW_LENGTH = 512
    
    # Dashboard Settings
    DASHBOARD_TITLE = "AI-Powered Consumer Insights Platform"
    DASHBOARD_SUBTITLE = "Real-time Amazon Review Analysis & Business Intelligence"
    
    # File Paths
    DATA_DIR = "../raw"
    OUTPUT_DIR = "outputs"
    MODELS_DIR = "models"
    
    # Analysis Settings
    MIN_REVIEWS_PER_PRODUCT = 5
    CONFIDENCE_THRESHOLD = 0.7
