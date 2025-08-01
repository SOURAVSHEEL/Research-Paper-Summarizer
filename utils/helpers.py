import os
import streamlit as st

def validate_api_key():
    """Validate Google API key availability"""
    return bool(os.getenv("GOOGLE_API_KEY"))

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def estimate_processing_time(text_length):
    """Estimate processing time based on text length"""
    # Rough estimate: 1000 characters per second
    seconds = text_length / 1000
    if seconds < 60:
        return f"~{int(seconds)} seconds"
    else:
        minutes = seconds / 60
        return f"~{int(minutes)} minutes"
