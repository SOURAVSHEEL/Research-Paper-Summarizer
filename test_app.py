import streamlit as st
import tempfile
import os
from io import BytesIO
from pathlib import Path
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import time
import json
import base64
from dotenv import load_dotenv

load_dotenv()

# Configure the page
st.set_page_config(
    page_title="AI Research Paper Summarizer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

import streamlit as st
import os
import PyPDF2
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
import time

# Set page configuration
st.set_page_config(
    page_title="PDF Research Paper Summarizer",
    page_icon="📄",
    layout="wide"
)

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def initialize_chat_llm():
    """Initialize ChatGoogleGenerativeAI"""
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
            max_retries=3
        )
        return llm
    except Exception as e:
        st.error(f"Error initializing ChatGoogleGenerativeAI: {str(e)}")
        return None

def summarize_text_chunk(llm, text):
    """Summarize a single text chunk using ChatGoogleGenerativeAI"""
    messages = [
        SystemMessage(content="""You are an expert academic researcher. Create comprehensive, well-structured summaries of research papers that help readers understand key concepts, methodology, findings, and implications."""),
        HumanMessage(content=f"""Please provide a comprehensive summary of this research paper text. Structure your summary with the following sections:

**TITLE & AUTHORS**: Extract the title and authors if available
**ABSTRACT/OVERVIEW**: Main purpose and scope of the research
**RESEARCH OBJECTIVES**: Key questions or hypotheses being investigated
**METHODOLOGY**: Research methods, data collection, and analysis approaches
**KEY FINDINGS**: Main results and discoveries
**CONCLUSIONS**: Primary conclusions and their significance
**IMPLICATIONS**: Broader impact and future research directions
**LIMITATIONS**: Any noted limitations or areas for improvement

Text to summarize:
{text}""")
    ]
    
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

def create_final_summary(llm, chunk_summaries):
    """Combine multiple chunk summaries into a final comprehensive summary"""
    combined_text = "\n\n---SECTION BREAK---\n\n".join(chunk_summaries)
    
    messages = [
        SystemMessage(content="""You are an expert academic researcher. Your task is to synthesize multiple section summaries into one comprehensive, coherent final summary."""),
        HumanMessage(content=f"""Please create a comprehensive final summary by synthesizing these section summaries from a research paper. Eliminate redundancy and create a flowing, coherent summary with the following structure:

**TITLE & AUTHORS**: Consolidated title and author information
**ABSTRACT/OVERVIEW**: Unified overview of the research
**RESEARCH OBJECTIVES**: Combined research questions and hypotheses
**METHODOLOGY**: Comprehensive methodology description
**KEY FINDINGS**: All important results and discoveries
**CONCLUSIONS**: Unified conclusions and their significance
**IMPLICATIONS**: Overall impact and future directions
**LIMITATIONS**: All noted limitations

Section summaries to synthesize:
{combined_text}""")
    ]
    
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        st.error(f"Error creating final summary: {str(e)}")
        return None

def chunk_text(text, chunk_size=4000, overlap=500):
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def process_document(text, llm):
    """Process the entire document and generate summary"""
    
    # If text is short enough, process as single chunk
    if len(text) <= 15000:
        st.write("📄 Processing document as single chunk...")
        with st.spinner("Generating summary..."):
            return summarize_text_chunk(llm, text)
    
    # Process in multiple chunks
    chunks = chunk_text(text, chunk_size=4000, overlap=500)
    st.write(f"📄 Processing document in {len(chunks)} chunks...")
    
    chunk_summaries = []
    progress_bar = st.progress(0)
    
    # Process each chunk
    for i, chunk in enumerate(chunks):
        with st.spinner(f"Processing chunk {i+1}/{len(chunks)}..."):
            summary = summarize_text_chunk(llm, chunk)
            if summary:
                chunk_summaries.append(summary)
            
            progress_bar.progress((i + 1) / len(chunks))
            time.sleep(1)  # Rate limiting
    
    # Create final comprehensive summary
    if chunk_summaries:
        st.write("🔗 Creating final comprehensive summary...")
        with st.spinner("Synthesizing all sections..."):
            return create_final_summary(llm, chunk_summaries)
    
    return None

# Streamlit UI
st.title("📄 PDF Research Paper Summarizer")
st.markdown("**Powered by ChatGoogleGenerativeAI**")

# API Key input
if not os.getenv("GOOGLE_API_KEY"):
    api_key = st.text_input(
        "🔑 Enter your Google API Key:", 
        type="password", 
        help="Get your API key from https://ai.google.dev/"
    )
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.rerun()
else:
    st.success("✅ Google API Key loaded")

# File upload
uploaded_file = st.file_uploader(
    "📎 Upload your research paper (PDF)", 
    type=['pdf'],
    help="Upload a PDF file to generate an AI-powered summary"
)

# Main processing
if uploaded_file is not None and os.getenv("GOOGLE_API_KEY"):
    
    # Display file info
    st.success(f"✅ **File uploaded:** {uploaded_file.name}")
    
    # Settings
    with st.expander("⚙️ Advanced Settings"):
        chunk_size = st.slider("Chunk Size", 2000, 6000, 4000, 500)
        chunk_overlap = st.slider("Chunk Overlap", 200, 1000, 500, 100)
    
    if st.button("🚀 Generate Summary", type="primary"):
        
        # Initialize ChatGoogleGenerativeAI
        llm = initialize_chat_llm()
        
        if llm is None:
            st.error("❌ Failed to initialize ChatGoogleGenerativeAI. Check your API key.")
        else:
            st.success("✅ **ChatGoogleGenerativeAI initialized**")
            
            # Extract text from PDF
            with st.spinner("📖 Extracting text from PDF..."):
                text = extract_text_from_pdf(uploaded_file)
            
            if text:
                st.success(f"✅ **Text extracted:** {len(text):,} characters")
                
                # Show text preview
                with st.expander("👀 Preview extracted text"):
                    st.text(text[:1000] + "..." if len(text) > 1000 else text)
                
                # Generate summary
                summary = process_document(text, llm)
                
                if summary:
                    st.success("✅ **Summary generated successfully!**")
                    
                    # Display summary
                    st.markdown("## 📋 Research Paper Summary")
                    st.markdown(summary)
                    
                    # Download button
                    st.download_button(
                        label="💾 Download Summary",
                        data=summary,
                        file_name=f"summary_{uploaded_file.name.replace('.pdf', '.txt')}",
                        mime="text/plain"
                    )
                    
                    # Statistics
                    with st.expander("📊 Summary Statistics"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Characters", f"{len(text):,}")
                        with col2:
                            st.metric("Summary Characters", f"{len(summary):,}")
                        with col3:
                            compression_ratio = round((1 - len(summary)/len(text)) * 100, 1)
                            st.metric("Compression", f"{compression_ratio}%")
                
                else:
                    st.error("❌ Failed to generate summary")
            else:
                st.error("❌ Failed to extract text from PDF")

elif uploaded_file is not None:
    st.warning("⚠️ Please enter your Google API Key to proceed")
else:
    st.info("👆 Please upload a PDF file to get started")

# Sidebar information
with st.sidebar:
    st.markdown("### 🔧 How it works")
    st.markdown("""
    1. **Upload PDF**: Choose your research paper
    2. **Text Extraction**: Extract text using PyPDF2
    3. **Smart Chunking**: Split large documents efficiently
    4. **ChatGoogleGenerativeAI**: Generate structured summaries
    5. **Final Synthesis**: Combine chunks into comprehensive summary
    """)
    
    st.markdown("### ⚡ Features")
    st.markdown("""
    - ✅ **ChatGoogleGenerativeAI** powered
    - ✅ Handles large research papers
    - ✅ Structured academic summaries
    - ✅ Progress tracking
    - ✅ Configurable chunking
    - ✅ Download summaries
    - ✅ Compression statistics
    """)
    
    st.markdown("### 🎯 Model Details")
    st.markdown("""
    - **Model**: gemini-2.0-flash
    - **Temperature**: 0.2 (focused)
    - **Max Retries**: 3
    - **Rate Limited**: Yes
    """)
