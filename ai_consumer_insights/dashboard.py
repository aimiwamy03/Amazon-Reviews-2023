"""
AI-Powered Consumer Insights Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from typing import Dict, List

# Import our custom modules
from data_processor import AmazonDataProcessor
from sentiment_analyzer import AdvancedSentimentAnalyzer
from topic_analyzer import ConsumerTopicAnalyzer
from insight_generator import AIInsightGenerator
from config import Config

class ConsumerInsightsDashboard:
    def __init__(self):
        self.config = Config()
        self.data_processor = AmazonDataProcessor()
        self.sentiment_analyzer = AdvancedSentimentAnalyzer()
        self.topic_analyzer = ConsumerTopicAnalyzer()
        self.insight_generator = AIInsightGenerator()
        
        # Initialize session state
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
    
    def run(self):
        """Main dashboard application"""
        st.set_page_config(
            page_title=self.config.DASHBOARD_TITLE,
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Header
        st.title("🤖 AI-Powered Consumer Insights Platform")
        st.markdown("### Real-time Amazon Review Analysis & Business Intelligence")
        st.markdown("---")
        
        # Sidebar
        self._create_sidebar()
        
        # Main content
        if st.session_state.data_loaded:
            self._display_main_content()
        else:
            self._display_welcome_screen()
    
    def _create_sidebar(self):
        """Create sidebar with controls"""
        st.sidebar.title("🎛️ Control Panel")
        
        # Data loading section
        st.sidebar.subheader("📊 Data Management")
        
        if st.sidebar.button("🔄 Load Sample Data", type="primary"):
            self._load_and_analyze_data()
        
        if st.sidebar.button("🧹 Clear Data"):
            st.session_state.data_loaded = False
            st.session_state.analysis_results = None
            st.rerun()
        
        # Analysis options
        st.sidebar.subheader("🔍 Analysis Options")
        
        self.show_sentiment_analysis = st.sidebar.checkbox("Sentiment Analysis", value=True)
        self.show_topic_modeling = st.sidebar.checkbox("Topic Modeling", value=True)
        self.show_product_insights = st.sidebar.checkbox("Product Insights", value=True)
        self.show_market_analysis = st.sidebar.checkbox("Market Analysis", value=True)
        
        # Display options
        st.sidebar.subheader("📈 Display Options")
        self.chart_style = st.sidebar.selectbox("Chart Style", ["plotly", "streamlit"])
        self.color_scheme = st.sidebar.selectbox("Color Scheme", ["viridis", "plasma", "inferno", "magma"])
    
    def _display_welcome_screen(self):
        """Display welcome screen with instructions"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ## 🚀 Welcome to AI Consumer Insights Platform
            
            This platform uses advanced AI to analyze consumer reviews and generate actionable business insights.
            
            ### 🎯 Key Features:
            - **Advanced Sentiment Analysis** using RoBERTa
            - **Intelligent Topic Modeling** with BERTopic
            - **AI-Generated Business Insights**
            - **Real-time Market Analysis**
            - **Product Performance Tracking**
            
            ### 🚀 Getting Started:
            1. Click "Load Sample Data" in the sidebar
            2. Wait for AI analysis to complete
            3. Explore insights and recommendations
            
            ### 💡 Use Cases:
            - Product strategy optimization
            - Customer satisfaction monitoring
            - Market trend identification
            - Competitive analysis
            - Business intelligence reporting
            """)
            
            st.info("💡 **Tip**: The platform uses sample Amazon review data for demonstration. In production, it would connect to real-time data sources.")
    
    def _load_and_analyze_data(self):
        """Load and analyze data with progress indicators"""
        with st.spinner("🔄 Loading and analyzing data..."):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Load data
                status_text.text("📊 Loading sample data...")
                progress_bar.progress(20)
                reviews_df, metadata_df = self.data_processor.load_sample_data()
                
                # Step 2: Preprocess data
                status_text.text("🧹 Preprocessing data...")
                progress_bar.progress(40)
                reviews_df = self.data_processor.preprocess_reviews(reviews_df)
                
                # Step 3: Sentiment analysis
                status_text.text("😊 Running sentiment analysis...")
                progress_bar.progress(60)
                sentiment_results = self.sentiment_analyzer.analyze_sentiment_evolution(reviews_df)
                
                # Step 4: Topic modeling
                status_text.text("🔍 Extracting topics...")
                progress_bar.progress(80)
                topic_results = self.topic_analyzer.extract_consumer_topics(reviews_df)
                topic_insights = self.topic_analyzer.get_topic_insights(topic_results['topic_analysis'])
                topic_recommendations = self.topic_analyzer.generate_topic_recommendations(topic_insights)
                
                # Step 5: Generate insights
                status_text.text("🧠 Generating AI insights...")
                progress_bar.progress(100)
                
                # Store results
                st.session_state.analysis_results = {
                    'reviews_data': reviews_df,
                    'metadata': metadata_df,
                    'sentiment_analysis': sentiment_results,
                    'topic_analysis': topic_results,
                    'topic_insights': topic_insights,
                    'topic_recommendations': topic_recommendations
                }
                
                st.session_state.data_loaded = True
                status_text.text("✅ Analysis complete!")
                
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                status_text.text("❌ Analysis failed")
    
    def _display_main_content(self):
        """Display main dashboard content"""
        results = st.session_state.analysis_results
        
        # Executive Summary
        st.subheader("📋 Executive Summary")
        executive_summary = self.insight_generator.generate_executive_summary(results)
        st.markdown(executive_summary)
        
        st.markdown("---")
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "😊 Sentiment Analysis", 
            "🔍 Topic Modeling", 
            "📈 Product Insights", 
            "🎯 Market Analysis"
        ])
        
        with tab1:
            self._display_overview_tab(results)
        
        with tab2:
            if self.show_sentiment_analysis:
                self._display_sentiment_tab(results)
            else:
                st.info("Sentiment analysis is disabled in the sidebar")
        
        with tab3:
            if self.show_topic_modeling:
                self._display_topic_tab(results)
            else:
                st.info("Topic modeling is disabled in the sidebar")
        
        with tab4:
            if self.show_product_insights:
                self._display_product_tab(results)
            else:
                st.info("Product insights are disabled in the sidebar")
        
        with tab5:
            if self.show_market_analysis:
                self._display_market_tab(results)
            else:
                st.info("Market analysis is disabled in the sidebar")
    
    def _display_overview_tab(self, results: Dict):
        """Display overview tab with key metrics"""
        reviews_df = results['reviews_data']
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Reviews", f"{len(reviews_df):,}")
        
        with col2:
            avg_rating = reviews_df['rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
        
        with col3:
            sentiment_dist = results['sentiment_analysis']['overall_sentiment_distribution']
            positive_pct = (sentiment_dist.get('positive', 0) / sum(sentiment_dist.values())) * 100
            st.metric("Positive Sentiment", f"{positive_pct:.1f}%")
        
        with col4:
            unique_products = reviews_df['product_name'].nunique()
            st.metric("Products Analyzed", f"{unique_products}")
        
        # Rating distribution
        st.subheader("📊 Rating Distribution")
        rating_counts = reviews_df['rating'].value_counts().sort_index()
        
        fig_ratings = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            title="Review Rating Distribution",
            labels={'x': 'Rating', 'y': 'Number of Reviews'},
            color=rating_counts.values,
            color_continuous_scale=self.color_scheme
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
        
        # Top products
        st.subheader("🏆 Top Performing Products")
        product_summary = self.data_processor.get_product_summary(reviews_df)
        top_products = product_summary.nlargest(5, 'avg_rating')
        
        fig_products = px.bar(
            top_products,
            x='avg_rating',
            y='product_name',
            orientation='h',
            title="Top Products by Average Rating",
            labels={'avg_rating': 'Average Rating', 'product_name': 'Product'},
            color='avg_rating',
            color_continuous_scale=self.color_scheme
        )
        st.plotly_chart(fig_products, use_container_width=True)
    
    def _display_sentiment_tab(self, results: Dict):
        """Display sentiment analysis tab"""
        sentiment_data = results['sentiment_analysis']
        
        # Sentiment distribution
        st.subheader("😊 Sentiment Distribution")
        sentiment_dist = sentiment_data['overall_sentiment_distribution']
        
        fig_sentiment = px.pie(
            values=list(sentiment_dist.values()),
            names=list(sentiment_dist.keys()),
            title="Overall Sentiment Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Sentiment trends over time
        if 'sentiment_trends' in sentiment_data:
            st.subheader("📈 Sentiment Trends Over Time")
            trends_df = sentiment_data['sentiment_trends']
            
            fig_trends = px.line(
                trends_df,
                x='month',
                y='sentiment',
                title="Sentiment Trends Over Time",
                labels={'sentiment': 'Positive Sentiment %', 'month': 'Month'}
            )
            st.plotly_chart(fig_trends, use_container_width=True)
        
        # Sentiment by rating
        if 'sentiment_by_rating' in sentiment_data:
            st.subheader("🎯 Sentiment vs Rating Analysis")
            sentiment_by_rating = sentiment_data['sentiment_by_rating']
            
            fig_sentiment_rating = px.bar(
                sentiment_by_rating,
                title="Sentiment Distribution by Rating",
                labels={'index': 'Rating', 'value': 'Count'},
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_sentiment_rating, use_container_width=True)
    
    def _display_topic_tab(self, results: Dict):
        """Display topic modeling tab"""
        topic_data = results['topic_analysis']
        topic_insights = results['topic_insights']
        
        # Topic distribution
        st.subheader("🔍 Discovered Topics")
        topic_info = topic_data['topic_info']
        
        # Filter out outlier topic (-1)
        topic_info_filtered = topic_info[topic_info['Topic'] != -1]
        
        fig_topics = px.bar(
            topic_info_filtered,
            x='Topic',
            y='Count',
            title="Topic Distribution",
            labels={'Topic': 'Topic ID', 'Count': 'Number of Reviews'},
            color='Count',
            color_continuous_scale=self.color_scheme
        )
        st.plotly_chart(fig_topics, use_container_width=True)
        
        # High impact topics
        st.subheader("⭐ High Impact Topics")
        high_impact_topics = topic_insights.get('high_impact_topics', [])
        
        if high_impact_topics:
            for i, topic in enumerate(high_impact_topics[:5]):
                with st.expander(f"Topic {topic['topic_id']}: {', '.join(topic['words'][:3])}"):
                    st.write(f"**Impact Score:** {topic['impact_score']:.1f}")
                    st.write(f"**Key Words:** {', '.join(topic['words'])}")
                    st.write(f"**Insight:** {topic['insight']}")
        else:
            st.info("No high impact topics identified")
        
        # Problem areas
        st.subheader("⚠️ Problem Areas")
        problem_areas = topic_insights.get('problem_areas', [])
        
        if problem_areas:
            for i, problem in enumerate(problem_areas[:3]):
                with st.expander(f"Problem Area {problem['topic_id']}: {', '.join(problem['words'][:3])}"):
                    st.write(f"**Problem Score:** {problem['problem_score']:.1f}")
                    st.write(f"**Key Words:** {', '.join(problem['words'])}")
                    st.write(f"**Issue:** {problem['insight']}")
        else:
            st.success("No significant problem areas identified")
        
        # Recommendations
        st.subheader("💡 AI Recommendations")
        recommendations = results.get('topic_recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.info("No specific recommendations generated")
    
    def _display_product_tab(self, results: Dict):
        """Display product insights tab"""
        reviews_df = results['reviews_data']
        
        # Product selector
        st.subheader("📦 Product Analysis")
        products = reviews_df['product_name'].unique()
        selected_product = st.selectbox("Select a product to analyze:", products)
        
        if selected_product:
            product_reviews = reviews_df[reviews_df['product_name'] == selected_product]
            product_insights = self.insight_generator.generate_product_insights(product_reviews)
            
            if selected_product in product_insights:
                insights = product_insights[selected_product]
                
                # Product metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Reviews", insights['total_reviews'])
                
                with col2:
                    st.metric("Average Rating", f"{insights['average_rating']:.1f}/5.0")
                
                with col3:
                    st.metric("Rating Trend", insights['rating_trend'])
                
                # Strengths and improvements
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("💪 Strengths")
                    for strength in insights['key_strengths']:
                        st.write(f"• {strength}")
                
                with col2:
                    st.subheader("🔧 Areas for Improvement")
                    for improvement in insights['improvement_areas']:
                        st.write(f"• {improvement}")
                
                # Recommendations
                st.subheader("🎯 Recommendations")
                for rec in insights['recommendations']:
                    st.write(f"• {rec}")
    
    def _display_market_tab(self, results: Dict):
        """Display market analysis tab"""
        market_insights = self.insight_generator.generate_market_insights(results)
        
        # Market sentiment
        st.subheader("🌍 Market Sentiment")
        st.write(market_insights['market_sentiment'])
        
        # Competitive positioning
        st.subheader("🏆 Competitive Positioning")
        st.write(market_insights['competitive_positioning'])
        
        # Growth opportunities
        st.subheader("🚀 Growth Opportunities")
        opportunities = market_insights['growth_opportunities']
        if opportunities:
            for i, opp in enumerate(opportunities, 1):
                st.write(f"{i}. {opp}")
        else:
            st.info("No specific growth opportunities identified")
        
        # Risk factors
        st.subheader("⚠️ Risk Factors")
        risks = market_insights['risk_factors']
        if risks:
            for i, risk in enumerate(risks, 1):
                st.write(f"{i}. {risk}")
        else:
            st.success("No significant risk factors identified")

def main():
    """Main application entry point"""
    dashboard = ConsumerInsightsDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
