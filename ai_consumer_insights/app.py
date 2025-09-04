"""
AI Consumer Insights Platform - Streamlit App
Optimized for Streamlit Community Cloud deployment
"""
import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules with error handling
try:
    from dashboard import main
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please check that all required files are present.")
    st.stop()

if __name__ == "__main__":
    main()
