"""
Topic Modeling and Consumer Insight Extraction using BERTopic
"""
import pandas as pd
import numpy as np
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple
import plotly.express as px
import plotly.graph_objects as go
from config import Config

class ConsumerTopicAnalyzer:
    def __init__(self):
        self.config = Config()
        
        # Initialize sentence transformer for embeddings
        self.embedding_model = SentenceTransformer(self.config.EMBEDDING_MODEL)
        
        # Initialize BERTopic
        self.topic_model = BERTopic(
            embedding_model=self.embedding_model,
            nr_topics="auto",  # Let AI determine optimal number of topics
            calculate_probabilities=True,
            verbose=True
        )
        
        self.topics = None
        self.topic_info = None
        
    def extract_consumer_topics(self, reviews_df: pd.DataFrame) -> Dict:
        """Extract topics from consumer reviews"""
        # Prepare text data
        review_texts = reviews_df['review_text_clean'].tolist()
        
        # Fit the topic model
        topics, probabilities = self.topic_model.fit_transform(review_texts)
        
        # Get topic information
        self.topic_info = self.topic_model.get_topic_info()
        
        # Add topics to dataframe
        reviews_df['topic_id'] = topics
        reviews_df['topic_probability'] = [max(probs) if probs else 0 for probs in probabilities]
        
        # Analyze topics
        topic_analysis = self._analyze_topics(reviews_df)
        
        return {
            'topic_info': self.topic_info,
            'topic_analysis': topic_analysis,
            'reviews_with_topics': reviews_df,
            'topic_visualization': self._create_topic_visualization()
        }
    
    def _analyze_topics(self, reviews_df: pd.DataFrame) -> Dict:
        """Analyze extracted topics for business insights"""
        topic_analysis = {}
        
        for topic_id in reviews_df['topic_id'].unique():
            if topic_id == -1:  # Skip outlier topic
                continue
                
            topic_reviews = reviews_df[reviews_df['topic_id'] == topic_id]
            
            # Get topic words
            topic_words = self.topic_model.get_topic(topic_id)
            
            # Analyze sentiment by topic
            sentiment_dist = topic_reviews['sentiment_label'].value_counts(normalize=True).to_dict()
            
            # Analyze ratings by topic
            avg_rating = topic_reviews['rating'].mean()
            rating_dist = topic_reviews['rating'].value_counts().to_dict()
            
            # Get representative reviews
            representative_reviews = topic_reviews.nlargest(3, 'topic_probability')['review_text'].tolist()
            
            topic_analysis[topic_id] = {
                'topic_words': [word for word, score in topic_words[:10]],  # Top 10 words
                'word_scores': dict(topic_words[:10]),
                'review_count': len(topic_reviews),
                'avg_rating': round(avg_rating, 2),
                'sentiment_distribution': sentiment_dist,
                'rating_distribution': rating_dist,
                'representative_reviews': representative_reviews,
                'avg_confidence': topic_reviews['topic_probability'].mean()
            }
        
        return topic_analysis
    
    def _create_topic_visualization(self) -> Dict:
        """Create visualizations for topics"""
        if self.topic_info is None:
            return {}
        
        # Topic size visualization
        topic_sizes = self.topic_info[self.topic_info['Topic'] != -1].copy()
        
        fig_topic_sizes = px.bar(
            topic_sizes, 
            x='Topic', 
            y='Count',
            title='Topic Distribution',
            labels={'Topic': 'Topic ID', 'Count': 'Number of Reviews'}
        )
        
        return {
            'topic_sizes_chart': fig_topic_sizes,
            'topic_info_table': self.topic_info
        }
    
    def get_topic_insights(self, topic_analysis: Dict) -> Dict:
        """Generate business insights from topic analysis"""
        insights = {
            'high_impact_topics': [],
            'problem_areas': [],
            'opportunities': [],
            'trending_topics': []
        }
        
        for topic_id, analysis in topic_analysis.items():
            # High impact topics (many reviews, high ratings)
            if analysis['review_count'] > 50 and analysis['avg_rating'] > 4.0:
                insights['high_impact_topics'].append({
                    'topic_id': topic_id,
                    'words': analysis['topic_words'][:5],
                    'impact_score': analysis['review_count'] * analysis['avg_rating'],
                    'insight': f"High-performing topic with {analysis['review_count']} reviews and {analysis['avg_rating']} avg rating"
                })
            
            # Problem areas (low ratings, negative sentiment)
            if analysis['avg_rating'] < 3.0 or analysis['sentiment_distribution'].get('negative', 0) > 0.4:
                insights['problem_areas'].append({
                    'topic_id': topic_id,
                    'words': analysis['topic_words'][:5],
                    'problem_score': analysis['review_count'] * (5 - analysis['avg_rating']),
                    'insight': f"Problem area with {analysis['avg_rating']} avg rating and {analysis['sentiment_distribution'].get('negative', 0):.1%} negative sentiment"
                })
            
            # Opportunities (moderate performance, room for improvement)
            if 3.0 <= analysis['avg_rating'] <= 4.0 and analysis['review_count'] > 20:
                insights['opportunities'].append({
                    'topic_id': topic_id,
                    'words': analysis['topic_words'][:5],
                    'opportunity_score': analysis['review_count'] * (5 - analysis['avg_rating']),
                    'insight': f"Improvement opportunity with {analysis['avg_rating']} avg rating and {analysis['review_count']} reviews"
                })
        
        # Sort by impact/problem/opportunity scores
        insights['high_impact_topics'].sort(key=lambda x: x['impact_score'], reverse=True)
        insights['problem_areas'].sort(key=lambda x: x['problem_score'], reverse=True)
        insights['opportunities'].sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return insights
    
    def extract_feature_sentiment(self, reviews_df: pd.DataFrame) -> Dict:
        """Extract sentiment for specific product features"""
        # Define common product features to look for
        feature_keywords = {
            'quality': ['quality', 'durable', 'well-made', 'cheap', 'flimsy', 'sturdy'],
            'price': ['price', 'expensive', 'affordable', 'value', 'cost', 'worth'],
            'shipping': ['shipping', 'delivery', 'fast', 'slow', 'arrived', 'packaging'],
            'customer_service': ['service', 'support', 'helpful', 'unhelpful', 'response'],
            'ease_of_use': ['easy', 'simple', 'complicated', 'difficult', 'user-friendly'],
            'appearance': ['looks', 'design', 'beautiful', 'ugly', 'style', 'color']
        }
        
        feature_sentiment = {}
        
        for feature, keywords in feature_keywords.items():
            feature_reviews = []
            
            for _, review in reviews_df.iterrows():
                review_text = review['review_text_clean'].lower()
                
                # Check if any keywords are mentioned
                if any(keyword in review_text for keyword in keywords):
                    feature_reviews.append({
                        'review_text': review['review_text_clean'],
                        'rating': review['rating'],
                        'sentiment': review['sentiment_label'],
                        'confidence': review.get('confidence', 0.5)
                    })
            
            if feature_reviews:
                feature_df = pd.DataFrame(feature_reviews)
                feature_sentiment[feature] = {
                    'total_mentions': len(feature_reviews),
                    'avg_rating': feature_df['rating'].mean(),
                    'sentiment_distribution': feature_df['sentiment'].value_counts(normalize=True).to_dict(),
                    'representative_reviews': feature_df.nlargest(3, 'confidence')['review_text'].tolist()
                }
        
        return feature_sentiment
    
    def generate_topic_recommendations(self, topic_insights: Dict) -> List[str]:
        """Generate actionable recommendations based on topic analysis"""
        recommendations = []
        
        # Recommendations for high-impact topics
        for topic in topic_insights['high_impact_topics'][:3]:
            recommendations.append(
                f"Leverage success in '{', '.join(topic['words'][:3])}' topic - "
                f"consider expanding related products or features"
            )
        
        # Recommendations for problem areas
        for problem in topic_insights['problem_areas'][:3]:
            recommendations.append(
                f"Address issues in '{', '.join(problem['words'][:3])}' area - "
                f"investigate and improve product quality or customer experience"
            )
        
        # Recommendations for opportunities
        for opportunity in topic_insights['opportunities'][:3]:
            recommendations.append(
                f"Improve '{', '.join(opportunity['words'][:3])}' features - "
                f"potential for significant rating improvement"
            )
        
        return recommendations
