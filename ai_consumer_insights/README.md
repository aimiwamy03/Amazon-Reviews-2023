# AI-Powered Consumer Insights Platform

## 🚀 Overview

This is an advanced AI-powered consumer insights platform that analyzes Amazon reviews to generate actionable business intelligence. The platform uses state-of-the-art AI models including RoBERTa for sentiment analysis and BERTopic for topic modeling.

## 🎯 Key Features

- **Advanced Sentiment Analysis**: Uses RoBERTa model for nuanced sentiment understanding
- **Intelligent Topic Modeling**: BERTopic automatically discovers consumer discussion topics
- **AI-Generated Insights**: Automated business intelligence and recommendations
- **Real-time Dashboard**: Interactive Streamlit interface for data exploration
- **Product Performance Analysis**: Individual product insights and recommendations
- **Market Intelligence**: Competitive positioning and growth opportunity identification

## 🛠️ Technology Stack

- **NLP Models**: RoBERTa, BERTopic, Sentence Transformers
- **Framework**: Streamlit, Plotly
- **Data Processing**: Pandas, NumPy
- **AI Libraries**: Transformers, Torch
- **Visualization**: Plotly, Streamlit Charts

## 📦 Installation

1. **Clone the repository**:
   ```bash
   cd ai_consumer_insights
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model** (optional, for advanced NLP):
   ```bash
   python -m spacy download en_core_web_lg
   ```

## 🚀 Quick Start

1. **Run the application**:
   ```bash
   streamlit run main.py
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Load sample data** by clicking "Load Sample Data" in the sidebar

4. **Explore insights** across different tabs:
   - Overview: Key metrics and charts
   - Sentiment Analysis: AI-powered sentiment insights
   - Topic Modeling: Consumer discussion topics
   - Product Insights: Individual product analysis
   - Market Analysis: Strategic business intelligence

## 📊 Sample Data

The platform includes realistic sample data that mimics Amazon review structure:
- 1,000 sample reviews across 10 product categories
- Product metadata with ratings, descriptions, and features
- Timestamp data for trend analysis
- User interaction data (helpful votes, verified purchases)

## 🎯 Use Cases

### For MasterClass Consumer Insights Team:

1. **Product Strategy**: Identify high-performing features and improvement areas
2. **Market Intelligence**: Understand competitive positioning and market sentiment
3. **Customer Experience**: Monitor satisfaction trends and identify pain points
4. **Business Intelligence**: Generate executive-ready insights and recommendations
5. **Risk Management**: Early warning system for product or brand issues

## 🔧 Configuration

Edit `config.py` to customize:
- Model settings and API keys
- Data processing parameters
- Dashboard appearance
- Analysis thresholds

## 📈 Key Metrics

The platform tracks and analyzes:
- **Sentiment Distribution**: Positive, negative, neutral sentiment percentages
- **Rating Trends**: Average ratings and rating evolution over time
- **Topic Impact**: High-impact discussion topics and problem areas
- **Product Performance**: Individual product strengths and weaknesses
- **Market Position**: Competitive analysis and growth opportunities

## 🧠 AI Models Used

1. **RoBERTa Sentiment Analysis**: 
   - Model: `cardiffnlp/twitter-roberta-base-sentiment-latest`
   - Purpose: Advanced sentiment classification with confidence scores

2. **BERTopic Topic Modeling**:
   - Embedding Model: `all-MiniLM-L6-v2`
   - Purpose: Automatic topic discovery and consumer insight extraction

3. **Custom Insight Generation**:
   - Purpose: Business intelligence and strategic recommendations

## 📱 Dashboard Features

- **Interactive Charts**: Plotly-powered visualizations
- **Real-time Analysis**: Live sentiment and topic analysis
- **Export Capabilities**: Download insights and reports
- **Responsive Design**: Works on desktop and mobile
- **Customizable Views**: Toggle different analysis types

## 🎨 Customization

- **Color Schemes**: Choose from multiple color palettes
- **Chart Styles**: Switch between different visualization styles
- **Analysis Options**: Enable/disable specific analysis types
- **Data Sources**: Easily connect to different data sources

## 🔮 Future Enhancements

- Real-time data integration
- Advanced predictive modeling
- Multi-language support
- API endpoints for integration
- Advanced visualization options
- Custom model training

## 📞 Support

For questions or issues:
1. Check the configuration in `config.py`
2. Verify all dependencies are installed
3. Ensure sufficient system resources for AI models
4. Check the console for error messages

## 🏆 Business Value

This platform provides:
- **Data-Driven Decisions**: AI-powered insights for strategic planning
- **Competitive Advantage**: Understanding consumer sentiment and trends
- **Risk Mitigation**: Early identification of product or brand issues
- **Revenue Optimization**: Identifying growth opportunities and improvement areas
- **Customer Satisfaction**: Monitoring and improving customer experience

---

**Built with ❤️ for MasterClass Consumer Insights Team**
