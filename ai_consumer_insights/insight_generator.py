"""
AI-Powered Business Insight Generation System
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
from config import Config

class AIInsightGenerator:
    def __init__(self):
        self.config = Config()
        
    def generate_executive_summary(self, analysis_results: Dict) -> str:
        """Generate executive summary using AI-like logic"""
        
        # Extract key metrics
        sentiment_data = analysis_results.get('sentiment_analysis', {})
        topic_data = analysis_results.get('topic_analysis', {})
        
        total_reviews = len(analysis_results.get('reviews_data', []))
        avg_rating = analysis_results.get('reviews_data', pd.DataFrame())['rating'].mean() if not analysis_results.get('reviews_data', pd.DataFrame()).empty else 0
        
        # Generate summary
        summary = f"""
## Executive Summary

**Dataset Overview:**
- Analyzed {total_reviews:,} consumer reviews
- Average product rating: {avg_rating:.1f}/5.0
- Sentiment distribution: {self._get_sentiment_summary(sentiment_data)}

**Key Findings:**
{self._generate_key_findings(analysis_results)}

**Strategic Recommendations:**
{self._generate_strategic_recommendations(analysis_results)}

**Business Impact:**
{self._assess_business_impact(analysis_results)}
        """
        
        return summary.strip()
    
    def _get_sentiment_summary(self, sentiment_data: Dict) -> str:
        """Generate sentiment summary"""
        if not sentiment_data:
            return "Data not available"
        
        sentiment_dist = sentiment_data.get('overall_sentiment_distribution', {})
        total = sum(sentiment_dist.values())
        
        if total == 0:
            return "No sentiment data available"
        
        positive_pct = (sentiment_dist.get('positive', 0) / total) * 100
        negative_pct = (sentiment_dist.get('negative', 0) / total) * 100
        neutral_pct = (sentiment_dist.get('neutral', 0) / total) * 100
        
        return f"{positive_pct:.1f}% positive, {negative_pct:.1f}% negative, {neutral_pct:.1f}% neutral"
    
    def _generate_key_findings(self, analysis_results: Dict) -> str:
        """Generate key findings from analysis"""
        findings = []
        
        # Sentiment findings
        sentiment_data = analysis_results.get('sentiment_analysis', {})
        if sentiment_data:
            avg_confidence = sentiment_data.get('average_confidence', 0)
            findings.append(f"• Sentiment analysis confidence: {avg_confidence:.1%}")
        
        # Topic findings
        topic_insights = analysis_results.get('topic_insights', {})
        if topic_insights:
            high_impact_count = len(topic_insights.get('high_impact_topics', []))
            problem_count = len(topic_insights.get('problem_areas', []))
            findings.append(f"• Identified {high_impact_count} high-impact topics and {problem_count} problem areas")
        
        # Product performance findings
        reviews_df = analysis_results.get('reviews_data', pd.DataFrame())
        if not reviews_df.empty:
            top_products = reviews_df.groupby('product_name')['rating'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(3)
            findings.append(f"• Top performing products: {', '.join(top_products.index[:2])}")
        
        return '\n'.join(findings) if findings else "• Analysis in progress"
    
    def _generate_strategic_recommendations(self, analysis_results: Dict) -> str:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Topic-based recommendations
        topic_recommendations = analysis_results.get('topic_recommendations', [])
        if topic_recommendations:
            recommendations.extend(topic_recommendations[:3])
        
        # Sentiment-based recommendations
        sentiment_data = analysis_results.get('sentiment_analysis', {})
        if sentiment_data:
            sentiment_dist = sentiment_data.get('overall_sentiment_distribution', {})
            total = sum(sentiment_dist.values())
            
            if total > 0:
                negative_pct = (sentiment_dist.get('negative', 0) / total) * 100
                if negative_pct > 30:
                    recommendations.append("• Address negative sentiment by improving product quality and customer service")
                elif negative_pct < 15:
                    recommendations.append("• Maintain high satisfaction levels with current product strategy")
        
        # Rating-based recommendations
        reviews_df = analysis_results.get('reviews_data', pd.DataFrame())
        if not reviews_df.empty:
            avg_rating = reviews_df['rating'].mean()
            if avg_rating < 3.5:
                recommendations.append("• Focus on improving overall product quality to increase ratings")
            elif avg_rating > 4.2:
                recommendations.append("• Leverage high ratings for marketing and customer acquisition")
        
        return '\n'.join(recommendations) if recommendations else "• Continue monitoring consumer feedback trends"
    
    def _assess_business_impact(self, analysis_results: Dict) -> str:
        """Assess potential business impact"""
        impact_points = []
        
        # Review volume impact
        total_reviews = len(analysis_results.get('reviews_data', []))
        if total_reviews > 500:
            impact_points.append("High review volume indicates strong customer engagement")
        elif total_reviews > 100:
            impact_points.append("Moderate review volume suggests growing customer base")
        
        # Sentiment impact
        sentiment_data = analysis_results.get('sentiment_analysis', {})
        if sentiment_data:
            sentiment_dist = sentiment_data.get('overall_sentiment_distribution', {})
            total = sum(sentiment_dist.values())
            
            if total > 0:
                positive_pct = (sentiment_dist.get('positive', 0) / total) * 100
                if positive_pct > 60:
                    impact_points.append("Strong positive sentiment supports brand reputation and sales")
                elif positive_pct < 40:
                    impact_points.append("Negative sentiment trends may impact customer retention")
        
        # Topic impact
        topic_insights = analysis_results.get('topic_insights', {})
        if topic_insights:
            high_impact_topics = topic_insights.get('high_impact_topics', [])
            if high_impact_topics:
                impact_points.append(f"Identified {len(high_impact_topics)} high-impact areas for strategic focus")
        
        return '; '.join(impact_points) if impact_points else "Analysis provides foundation for data-driven decision making"
    
    def generate_product_insights(self, reviews_df: pd.DataFrame) -> Dict:
        """Generate insights for individual products"""
        if reviews_df.empty:
            return {}
        
        product_insights = {}
        
        for product in reviews_df['product_name'].unique():
            product_reviews = reviews_df[reviews_df['product_name'] == product]
            
            insights = {
                'total_reviews': len(product_reviews),
                'average_rating': product_reviews['rating'].mean(),
                'rating_std': product_reviews['rating'].std(),
                'sentiment_distribution': product_reviews['sentiment_label'].value_counts(normalize=True).to_dict(),
                'rating_trend': self._calculate_rating_trend(product_reviews),
                'key_strengths': self._identify_strengths(product_reviews),
                'improvement_areas': self._identify_improvements(product_reviews),
                'recommendations': self._generate_product_recommendations(product_reviews)
            }
            
            product_insights[product] = insights
        
        return product_insights
    
    def _calculate_rating_trend(self, product_reviews: pd.DataFrame) -> str:
        """Calculate rating trend for a product"""
        if len(product_reviews) < 10:
            return "Insufficient data for trend analysis"
        
        # Sort by timestamp and calculate rolling average
        product_reviews_sorted = product_reviews.sort_values('timestamp')
        
        if len(product_reviews_sorted) >= 20:
            recent_avg = product_reviews_sorted.tail(10)['rating'].mean()
            earlier_avg = product_reviews_sorted.head(10)['rating'].mean()
            
            if recent_avg > earlier_avg + 0.3:
                return "Improving trend"
            elif recent_avg < earlier_avg - 0.3:
                return "Declining trend"
            else:
                return "Stable trend"
        
        return "Stable trend"
    
    def _identify_strengths(self, product_reviews: pd.DataFrame) -> List[str]:
        """Identify product strengths from reviews"""
        strengths = []
        
        # High rating reviews
        high_rating_reviews = product_reviews[product_reviews['rating'] >= 4]
        if len(high_rating_reviews) > 0:
            strengths.append(f"Strong positive feedback ({len(high_rating_reviews)} high-rating reviews)")
        
        # Sentiment analysis
        positive_reviews = product_reviews[product_reviews['sentiment_label'] == 'positive']
        if len(positive_reviews) > len(product_reviews) * 0.6:
            strengths.append("Consistently positive sentiment")
        
        # Helpful votes
        avg_helpful = product_reviews['helpful_votes'].mean()
        if avg_helpful > 5:
            strengths.append("High review helpfulness")
        
        return strengths
    
    def _identify_improvements(self, product_reviews: pd.DataFrame) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        
        # Low rating reviews
        low_rating_reviews = product_reviews[product_reviews['rating'] <= 2]
        if len(low_rating_reviews) > 0:
            improvements.append(f"Address {len(low_rating_reviews)} low-rating reviews")
        
        # Negative sentiment
        negative_reviews = product_reviews[product_reviews['sentiment_label'] == 'negative']
        if len(negative_reviews) > len(product_reviews) * 0.3:
            improvements.append("Reduce negative sentiment")
        
        # Rating consistency
        rating_std = product_reviews['rating'].std()
        if rating_std > 1.5:
            improvements.append("Improve rating consistency")
        
        return improvements
    
    def _generate_product_recommendations(self, product_reviews: pd.DataFrame) -> List[str]:
        """Generate specific recommendations for a product"""
        recommendations = []
        
        avg_rating = product_reviews['rating'].mean()
        
        if avg_rating < 3.0:
            recommendations.append("Urgent: Focus on fundamental product quality improvements")
        elif avg_rating < 4.0:
            recommendations.append("Moderate: Enhance product features and customer experience")
        else:
            recommendations.append("Maintain: Continue current product strategy")
        
        # Sentiment-based recommendations
        sentiment_dist = product_reviews['sentiment_label'].value_counts(normalize=True)
        if sentiment_dist.get('negative', 0) > 0.3:
            recommendations.append("Address customer complaints and negative feedback")
        
        return recommendations
    
    def generate_market_insights(self, analysis_results: Dict) -> Dict:
        """Generate market-level insights"""
        market_insights = {
            'market_sentiment': self._assess_market_sentiment(analysis_results),
            'competitive_positioning': self._assess_competitive_position(analysis_results),
            'growth_opportunities': self._identify_growth_opportunities(analysis_results),
            'risk_factors': self._identify_risk_factors(analysis_results)
        }
        
        return market_insights
    
    def _assess_market_sentiment(self, analysis_results: Dict) -> str:
        """Assess overall market sentiment"""
        sentiment_data = analysis_results.get('sentiment_analysis', {})
        if not sentiment_data:
            return "Market sentiment data not available"
        
        sentiment_dist = sentiment_data.get('overall_sentiment_distribution', {})
        total = sum(sentiment_dist.values())
        
        if total == 0:
            return "No sentiment data available"
        
        positive_pct = (sentiment_dist.get('positive', 0) / total) * 100
        
        if positive_pct > 70:
            return "Highly positive market sentiment - strong customer satisfaction"
        elif positive_pct > 50:
            return "Moderately positive market sentiment - room for improvement"
        else:
            return "Concerning market sentiment - immediate attention required"
    
    def _assess_competitive_position(self, analysis_results: Dict) -> str:
        """Assess competitive positioning"""
        reviews_df = analysis_results.get('reviews_data', pd.DataFrame())
        if reviews_df.empty:
            return "Insufficient data for competitive analysis"
        
        avg_rating = reviews_df['rating'].mean()
        
        if avg_rating > 4.2:
            return "Strong competitive position with high customer satisfaction"
        elif avg_rating > 3.5:
            return "Moderate competitive position - focus on differentiation"
        else:
            return "Weak competitive position - significant improvements needed"
    
    def _identify_growth_opportunities(self, analysis_results: Dict) -> List[str]:
        """Identify growth opportunities"""
        opportunities = []
        
        # Topic-based opportunities
        topic_insights = analysis_results.get('topic_insights', {})
        if topic_insights:
            high_impact_topics = topic_insights.get('high_impact_topics', [])
            for topic in high_impact_topics[:3]:
                opportunities.append(f"Expand in '{', '.join(topic['words'][:2])}' area")
        
        # Rating-based opportunities
        reviews_df = analysis_results.get('reviews_data', pd.DataFrame())
        if not reviews_df.empty:
            avg_rating = reviews_df['rating'].mean()
            if avg_rating > 4.0:
                opportunities.append("Leverage high ratings for customer acquisition")
        
        return opportunities
    
    def _identify_risk_factors(self, analysis_results: Dict) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        
        # Sentiment risks
        sentiment_data = analysis_results.get('sentiment_analysis', {})
        if sentiment_data:
            sentiment_dist = sentiment_data.get('overall_sentiment_distribution', {})
            total = sum(sentiment_dist.values())
            
            if total > 0:
                negative_pct = (sentiment_dist.get('negative', 0) / total) * 100
                if negative_pct > 25:
                    risks.append("High negative sentiment may impact brand reputation")
        
        # Topic-based risks
        topic_insights = analysis_results.get('topic_insights', {})
        if topic_insights:
            problem_areas = topic_insights.get('problem_areas', [])
            if problem_areas:
                risks.append(f"{len(problem_areas)} identified problem areas require attention")
        
        return risks
