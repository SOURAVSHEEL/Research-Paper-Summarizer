import logging
import os
from datetime import datetime
import streamlit as st

def setup_logger():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create log filename with current date
    log_filename = f"document_summarizer_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Log application start
    logging.info("="*50)
    logging.info("Document Summarizer Application Started")
    logging.info(f"Log file: {log_filepath}")
    logging.info("="*50)

def log_info(message):
    """Log info message"""
    logging.info(message)

def log_error(message):
    """Log error message"""
    logging.error(message)

def log_warning(message):
    """Log warning message"""
    logging.warning(message)

def log_debug(message):
    """Log debug message"""
    logging.debug(message)

def get_log_stats():
    """Get logging statistics"""
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        return {"total_logs": 0, "latest_log": None}
    
    log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
    
    if not log_files:
        return {"total_logs": 0, "latest_log": None}
    
    latest_log = max(log_files, key=lambda f: os.path.getctime(os.path.join(logs_dir, f)))
    
    return {
        "total_logs": len(log_files),
        "latest_log": latest_log,
        "logs_directory": logs_dir
    }

def get_recent_logs(lines=50):
    """Get recent log entries"""
    logs_dir = "logs"
    log_filename = f"document_summarizer_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    
    if not os.path.exists(log_filepath):
        return "No logs available for today."
    
    try:
        with open(log_filepath, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            return ''.join(recent_lines)
    except Exception as e:
        return f"Error reading logs: {str(e)}"
