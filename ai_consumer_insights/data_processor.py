"""
Data processing pipeline for Amazon Reviews dataset
"""
import pandas as pd
import numpy as np
import json
import os
from typing import Dict, List, Tuple
from config import Config

class AmazonDataProcessor:
    def __init__(self):
        self.config = Config()
        self.reviews_data = None
        self.metadata = None
        
    def load_sample_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load sample data for demo purposes"""
        # Create sample data that mimics Amazon review structure
        sample_reviews = self._create_sample_reviews()
        sample_metadata = self._create_sample_metadata()
        
        self.reviews_data = pd.DataFrame(sample_reviews)
        self.metadata = pd.DataFrame(sample_metadata)
        
        return self.reviews_data, self.metadata
    
    def _create_sample_reviews(self) -> List[Dict]:
        """Create realistic sample review data"""
        import random
        from datetime import datetime, timedelta
        
        products = [
            "Wireless Bluetooth Headphones",
            "Organic Face Moisturizer", 
            "Smart Fitness Tracker",
            "Premium Coffee Beans",
            "LED Desk Lamp",
            "Yoga Mat Premium",
            "Protein Powder Vanilla",
            "Phone Case Clear",
            "Essential Oil Diffuser",
            "Resistance Bands Set"
        ]
        
        review_templates = {
            "positive": [
                "Absolutely love this product! Quality is amazing and exceeded my expectations.",
                "Perfect! Exactly what I was looking for. Highly recommend to anyone.",
                "Great value for money. Works perfectly and arrived quickly.",
                "Excellent product! Will definitely buy again. 5 stars!",
                "Outstanding quality and fast shipping. Very satisfied with purchase."
            ],
            "negative": [
                "Disappointed with the quality. Not worth the money at all.",
                "Product broke after just one week. Very poor quality.",
                "Not as described. Waste of money. Would not recommend.",
                "Terrible customer service and product quality is subpar.",
                "Overpriced for what you get. Look elsewhere for better options."
            ],
            "neutral": [
                "Product is okay, nothing special. Does the job but could be better.",
                "Average quality. Works as expected but nothing extraordinary.",
                "Decent product for the price. No major complaints but not amazing either.",
                "It's fine. Gets the job done but there are probably better options.",
                "Standard quality. Nothing to complain about but nothing to rave about either."
            ]
        }
        
        reviews = []
        for i in range(self.config.SAMPLE_SIZE):
            product = random.choice(products)
            sentiment = random.choices(
                ["positive", "negative", "neutral"], 
                weights=[0.6, 0.2, 0.2]
            )[0]
            
            review_text = random.choice(review_templates[sentiment])
            rating = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.1, 0.2, 0.3, 0.3])[0]
            
            # Add some variation to make it more realistic
            if random.random() > 0.7:
                review_text += f" The {product.lower()} is really {random.choice(['amazing', 'terrible', 'okay'])}."
            
            reviews.append({
                'review_id': f"review_{i:06d}",
                'product_name': product,
                'rating': rating,
                'review_text': review_text,
                'user_id': f"user_{random.randint(1000, 9999)}",
                'timestamp': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                'helpful_votes': random.randint(0, 50),
                'verified_purchase': random.choice([True, False])
            })
        
        return reviews
    
    def _create_sample_metadata(self) -> List[Dict]:
        """Create sample product metadata"""
        import random
        
        products = [
            "Wireless Bluetooth Headphones",
            "Organic Face Moisturizer", 
            "Smart Fitness Tracker",
            "Premium Coffee Beans",
            "LED Desk Lamp",
            "Yoga Mat Premium",
            "Protein Powder Vanilla",
            "Phone Case Clear",
            "Essential Oil Diffuser",
            "Resistance Bands Set"
        ]
        
        categories = ["Electronics", "Beauty", "Health", "Food", "Home", "Sports"]
        
        metadata = []
        for i, product in enumerate(products):
            metadata.append({
                'product_id': f"prod_{i:03d}",
                'product_name': product,
                'category': random.choice(categories),
                'price': round(random.uniform(10, 200), 2),
                'average_rating': round(random.uniform(3.0, 5.0), 1),
                'total_reviews': random.randint(50, 1000),
                'description': f"High-quality {product.lower()} designed for modern consumers.",
                'features': [
                    f"Premium {product.split()[0].lower()} technology",
                    "Durable construction",
                    "Easy to use",
                    "Great value"
                ]
            })
        
        return metadata
    
    def preprocess_reviews(self, reviews_df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess review data"""
        # Remove duplicates
        reviews_df = reviews_df.drop_duplicates(subset=['review_id'])
        
        # Clean text
        reviews_df['review_text_clean'] = reviews_df['review_text'].str.strip()
        
        # Add text length
        reviews_df['text_length'] = reviews_df['review_text_clean'].str.len()
        
        # Filter out very short reviews
        reviews_df = reviews_df[reviews_df['text_length'] > 10]
        
        # Add sentiment labels based on rating
        reviews_df['sentiment_label'] = reviews_df['rating'].apply(
            lambda x: 'positive' if x >= 4 else 'negative' if x <= 2 else 'neutral'
        )
        
        return reviews_df
    
    def get_product_summary(self, reviews_df: pd.DataFrame) -> pd.DataFrame:
        """Generate product-level summary statistics"""
        product_summary = reviews_df.groupby('product_name').agg({
            'rating': ['mean', 'count', 'std'],
            'review_text': 'count',
            'helpful_votes': 'sum',
            'sentiment_label': lambda x: x.value_counts().to_dict()
        }).round(2)
        
        # Flatten column names
        product_summary.columns = ['avg_rating', 'review_count', 'rating_std', 'total_reviews', 'helpful_votes', 'sentiment_dist']
        
        return product_summary.reset_index()
