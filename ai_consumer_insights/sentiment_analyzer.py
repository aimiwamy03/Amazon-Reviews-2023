"""
Advanced Sentiment Analysis using RoBERTa and other AI models
"""
import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import Dict, List, Tuple
import re
from config import Config

class AdvancedSentimentAnalyzer:
    def __init__(self):
        self.config = Config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize RoBERTa sentiment analysis
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=self.config.SENTIMENT_MODEL,
            device=0 if self.device == "cuda" else -1
        )
        
        # Initialize tokenizer for custom analysis
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.SENTIMENT_MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.config.SENTIMENT_MODEL)
        self.model.to(self.device)
        
    def analyze_review_sentiment(self, review_text: str) -> Dict:
        """Analyze sentiment of a single review"""
        # Clean and truncate text
        clean_text = self._clean_text(review_text)
        
        if len(clean_text) < 5:
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'scores': {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
            }
        
        # Get sentiment prediction
        result = self.sentiment_pipeline(clean_text)[0]
        
        # Map to our sentiment categories
        sentiment_mapping = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral', 
            'LABEL_2': 'positive'
        }
        
        sentiment = sentiment_mapping.get(result['label'], 'neutral')
        confidence = result['score']
        
        # Get detailed scores
        scores = self._get_detailed_scores(clean_text)
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'scores': scores,
            'raw_text': clean_text
        }
    
    def analyze_batch_sentiment(self, reviews: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple reviews efficiently"""
        results = []
        
        # Process in batches for efficiency
        batch_size = 32
        for i in range(0, len(reviews), batch_size):
            batch = reviews[i:i + batch_size]
            batch_results = self.sentiment_pipeline(batch)
            
            for j, result in enumerate(batch_results):
                sentiment_mapping = {
                    'LABEL_0': 'negative',
                    'LABEL_1': 'neutral',
                    'LABEL_2': 'positive'
                }
                
                sentiment = sentiment_mapping.get(result['label'], 'neutral')
                confidence = result['score']
                
                results.append({
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'original_text': batch[j]
                })
        
        return results
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Truncate if too long
        if len(text) > self.config.MAX_REVIEW_LENGTH:
            text = text[:self.config.MAX_REVIEW_LENGTH]
        
        return text
    
    def _get_detailed_scores(self, text: str) -> Dict:
        """Get detailed sentiment scores for all categories"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Map to sentiment labels
        scores = {
            'negative': float(probabilities[0][0]),
            'neutral': float(probabilities[0][1]),
            'positive': float(probabilities[0][2])
        }
        
        return scores
    
    def extract_emotional_indicators(self, review_text: str) -> Dict:
        """Extract emotional indicators from review text"""
        emotional_words = {
            'positive_emotions': ['love', 'amazing', 'excellent', 'perfect', 'fantastic', 'wonderful', 'great', 'awesome'],
            'negative_emotions': ['hate', 'terrible', 'awful', 'horrible', 'disappointed', 'frustrated', 'angry', 'upset'],
            'intensity_words': ['extremely', 'incredibly', 'absolutely', 'completely', 'totally', 'really', 'very', 'so']
        }
        
        text_lower = review_text.lower()
        
        indicators = {
            'positive_emotion_count': sum(1 for word in emotional_words['positive_emotions'] if word in text_lower),
            'negative_emotion_count': sum(1 for word in emotional_words['negative_emotions'] if word in text_lower),
            'intensity_count': sum(1 for word in emotional_words['intensity_words'] if word in text_lower),
            'exclamation_count': review_text.count('!'),
            'caps_ratio': sum(1 for c in review_text if c.isupper()) / len(review_text) if review_text else 0
        }
        
        return indicators
    
    def analyze_sentiment_evolution(self, reviews_df: pd.DataFrame) -> Dict:
        """Analyze how sentiment changes over time"""
        # Add sentiment analysis to reviews
        reviews_df['sentiment_analysis'] = reviews_df['review_text'].apply(
            lambda x: self.analyze_review_sentiment(x)
        )
        
        # Extract sentiment and confidence
        reviews_df['sentiment'] = reviews_df['sentiment_analysis'].apply(lambda x: x['sentiment'])
        reviews_df['confidence'] = reviews_df['sentiment_analysis'].apply(lambda x: x['confidence'])
        
        # Convert timestamp to datetime
        reviews_df['date'] = pd.to_datetime(reviews_df['timestamp'])
        
        # Group by time periods
        reviews_df['month'] = reviews_df['date'].dt.to_period('M')
        
        # Calculate sentiment trends
        sentiment_trends = reviews_df.groupby('month').agg({
            'sentiment': lambda x: (x == 'positive').mean(),
            'confidence': 'mean',
            'rating': 'mean'
        }).reset_index()
        
        return {
            'sentiment_trends': sentiment_trends,
            'overall_sentiment_distribution': reviews_df['sentiment'].value_counts().to_dict(),
            'average_confidence': reviews_df['confidence'].mean(),
            'sentiment_by_rating': reviews_df.groupby('rating')['sentiment'].value_counts().unstack(fill_value=0)
        }
