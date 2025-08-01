import streamlit as st
import os
from dotenv import load_dotenv
from src.ui_components import setup_page_config, render_sidebar, render_main_content
from src.document_processor import extract_text_from_document
from src.llm_handler import initialize_chat_llm, process_document
from utils.helpers import validate_api_key
from utils.logger import setup_logger, log_info, log_error

def main():
    # Initialize logging
    setup_logger()
    log_info("Application started")
    
    # Load environment variables from .env file
    load_dotenv()
    log_info("Environment variables loaded from .env file")
    
    # Setup page configuration
    setup_page_config()
    
    # API Key handling
    api_key_valid = validate_api_key()
    
    # Create layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        uploaded_file, chunk_size, chunk_overlap = render_sidebar()
    
    with col2:
        render_main_content(uploaded_file, chunk_size, chunk_overlap, api_key_valid)

if __name__ == "__main__":
    main()
