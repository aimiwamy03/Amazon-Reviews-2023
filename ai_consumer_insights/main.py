"""
AI-Powered Consumer Insights Platform - Main Application
"""
import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dashboard import main

if __name__ == "__main__":
    main()
