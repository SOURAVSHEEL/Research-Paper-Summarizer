import streamlit as st
import os
from utils.logger import log_info, log_error
from src.document_processor import get_document_info, extract_text_from_document
from src.llm_handler import initialize_chat_llm, process_document, chunk_text


def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Document Summarizer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Simple, clean CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .summary-box {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the collapsible sidebar with file upload and settings"""
    
    # Only render sidebar content if show_sidebar is True
    if not st.session_state.get('show_sidebar', True):
        return None, 4000, 500  # Return default values when sidebar is hidden
    
    # Sidebar header
    st.markdown("### 📁 Document Upload")
    
    # File Upload Section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose your document",
        type=['pdf', 'docx', 'doc', 'txt', 'md'],
        help="Upload your document in supported format"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display uploaded file info - only when file is uploaded
    if uploaded_file:
        doc_info = get_document_info(uploaded_file)
        
        # Calculate file_size_mb BEFORE using it
        file_size_mb = doc_info['size'] / (1024 * 1024)
        
        st.markdown('<div class="file-info">', unsafe_allow_html=True)
        st.markdown(f"**📄 {doc_info['name']}**")
        st.markdown(f"**Type:** {doc_info['type']} | **Size:** {file_size_mb:.2f} MB")
        if doc_info['pages'] > 0:
            st.markdown(f"**Pages:** {doc_info['pages']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Processing Settings
    st.markdown("### ⚙️ Settings")
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    
    chunk_size = st.slider(
        "Chunk Size",
        min_value=2000,
        max_value=6000,
        value=4000,
        step=500,
        help="Size of text chunks for processing"
    )
    
    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=200,
        max_value=1000,
        value=500,
        step=100,
        help="Overlap between chunks for context preservation"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return uploaded_file, chunk_size, chunk_overlap

def render_main_content(uploaded_file, chunk_size, chunk_overlap, api_key_valid):
    """Render the main content area with sidebar toggle"""
    

    # Header
    st.markdown("# Document Summarizer")
    st.markdown('<p class="subtitle">AI-powered document analysis with advanced summarization capabilities</p>', 
                unsafe_allow_html=True)
    
    if not api_key_valid:
        st.error("⚠️ Please ensure your Google API key is configured in the .env file to get started.")
        
        # Show setup guide
        with st.expander("🚀 Setup Guide", expanded=True):
            st.markdown("""
            **Step 1:** Get your free Google API key
            - Visit [Google AI Studio](https://ai.google.dev/)
            - Sign in with your Google account
            - Create a new API key
            
            **Step 2:** Configure your .env file
            - Create a `.env` file in the project root
            - Add: `GOOGLE_API_KEY=your_api_key_here`
            - Restart the application
            
            **Step 3:** Start summarizing!
            - Upload your document using the settings panel
            - Click "🚀 Generate Summary"
            """)
        return
    
    # Show upload instruction when sidebar is hidden and no file uploaded
    if not st.session_state.get('show_sidebar', True) and not uploaded_file:
        st.info("📁 Click 'Settings' button above to upload your document and configure processing options.")
    
    if not uploaded_file:
        # Clean welcome section
        st.markdown("""
        <div class="welcome-section">
            <h2 class="welcome-title">Welcome to Document Summarizer! 🎉</h2>
            <p class="welcome-subtitle">
                Upload your document and get intelligent AI-powered summaries in seconds
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature list
        st.markdown("""
        <div class="feature-list">
            <h3>🚀 What You'll Get:</h3>
            <ul>
                <li>📋 <strong>Structured Summary</strong> - Well-organized sections and key points</li>
                <li>🎯 <strong>Research Objectives</strong> - Clear understanding of goals and methodology</li>
                <li>📊 <strong>Key Findings</strong> - Important results and discoveries highlighted</li>
                <li>🚀 <strong>Implications</strong> - Future directions and broader impact</li>
                <li>💾 <strong>Downloadable</strong> - Save summaries for later reference</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        return
    
    # Generate Summary Button
    if st.button("🚀 Generate Summary", type="primary"):
        log_info(f"User initiated summary generation for {uploaded_file.name}")
        process_document_and_generate_summary(uploaded_file, chunk_size, chunk_overlap)

def process_document_and_generate_summary(uploaded_file, chunk_size, chunk_overlap):
    """Process document and generate summary with clean progress UI"""

    log_info(f"Starting document processing for {uploaded_file.name}")
    
    # Create progress container
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        
        # Step 1: Initialize LLM (silent)
        llm = initialize_chat_llm()
        if not llm:
            log_error("Failed to initialize ChatGoogleGenerativeAI")
            st.error("❌ Failed to initialize the AI model. Please check your API key in .env file.")
            return
        
        # Step 2: Extract text (silent)
        text = extract_text_from_document(uploaded_file)
        if not text:
            log_error(f"Failed to extract text from {uploaded_file.name}")
            st.error("❌ Failed to extract text from document. Please try a different file.")
            return
        
        # Step 3: Process document with clean progress display
        st.markdown('<p class="processing-text">🤖 Processing your document...</p>', unsafe_allow_html=True)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Determine processing approach
        if len(text) <= 15000:
            status_text.markdown("*Analyzing document structure and content...*")
            progress_bar.progress(50)
            log_info("Processing as single chunk")
        else:
            chunks = chunk_text(text, chunk_size, chunk_overlap)
            status_text.markdown(f"*Processing document in {len(chunks)} intelligent sections...*")
            progress_bar.progress(25)
            log_info(f"Processing in {len(chunks)} chunks")
        
        # Generate summary
        summary = process_document(text, llm, chunk_size, chunk_overlap, 
                                 progress_bar, status_text)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Clear progress and show results
    progress_container.empty()
    
    if summary:
        log_info("Summary generated successfully")
        display_summary_results(summary, uploaded_file, text)
    else:
        log_error("Failed to generate summary")
        st.error("❌ Failed to generate summary. Please try again.")

def display_summary_results(summary, uploaded_file, original_text):
    """Display the generated summary with clean styling"""
    st.success("✅ Summary generated successfully!")
    
    # Summary display with clean styling
    st.markdown('<div class="summary-container">', unsafe_allow_html=True)
    st.markdown("## 📋 Document Summary")
    st.markdown(summary)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        filename = uploaded_file.name.rsplit('.', 1)[0] + '_summary.txt'
        st.download_button(
            label="💾 Download Summary",
            data=summary,
            file_name=filename,
            mime="text/plain"
        )
        log_info(f"Summary download button created for {filename}")
    
    with col2:
        if st.button("🔄 New Summary"):
            log_info("User requested new summary generation")
            st.rerun()
    
    with col3:
        # Clean statistics
        with st.expander("📊 Analytics"):
            st.metric("Original", f"{len(original_text):,} chars", help="Characters in original document")
            st.metric("Summary", f"{len(summary):,} chars", help="Characters in generated summary")
            
            compression = round((1 - len(summary)/len(original_text)) * 100, 1)
            st.metric("Compression", f"{compression}%", help="Reduction in document size")
            
            reading_time = max(1, round(len(summary) / 200))  # ~200 words per minute
            st.metric("Read Time", f"{reading_time} min", help="Estimated reading time")
            
            log_info(f"Summary stats - Original: {len(original_text)}, Summary: {len(summary)}, Compression: {compression}%")
