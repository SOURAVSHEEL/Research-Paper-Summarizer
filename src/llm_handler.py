from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
import time
from utils.logger import log_info, log_error, log_warning

def initialize_chat_llm():
    """Initialize ChatGoogleGenerativeAI silently"""
    try:
        log_info("Initializing ChatGoogleGenerativeAI")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
            max_retries=3
        )
        log_info("ChatGoogleGenerativeAI initialized successfully")
        return llm
    except Exception as e:
        log_error(f"Failed to initialize ChatGoogleGenerativeAI: {str(e)}")
        return None

def chunk_text(text, chunk_size=4000, overlap=500):
    """Split text into manageable chunks"""
    log_info(f"Chunking text: {len(text)} characters into chunks of {chunk_size} with {overlap} overlap")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    
    log_info(f"Text split into {len(chunks)} chunks")
    return chunks

def summarize_text_chunk(llm, text, chunk_num=None):
    """Summarize a single text chunk"""
    chunk_info = f" (chunk {chunk_num})" if chunk_num else ""
    log_info(f"Starting summarization{chunk_info} - {len(text)} characters")
    
    messages = [
        SystemMessage(content="""You are an expert academic researcher. Create comprehensive, well-structured summaries of research papers that help readers understand key concepts, methodology, findings, and implications."""),
        HumanMessage(content=f"""Please provide a comprehensive summary of this document text. Structure your summary with the following sections:

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
        start_time = time.time()
        response = llm.invoke(messages)
        end_time = time.time()
        
        log_info(f"Summarization completed{chunk_info} in {end_time - start_time:.2f} seconds")
        log_info(f"Generated summary{chunk_info}: {len(response.content)} characters")
        
        return response.content
    except Exception as e:
        log_error(f"Error generating summary{chunk_info}: {str(e)}")
        return None

def create_final_summary(llm, chunk_summaries):
    """Combine multiple chunk summaries into a final comprehensive summary"""
    log_info(f"Creating final summary from {len(chunk_summaries)} chunk summaries")
    
    combined_text = "\n\n---SECTION BREAK---\n\n".join(chunk_summaries)
    
    messages = [
        SystemMessage(content="""You are an expert academic researcher. Your task is to synthesize multiple section summaries into one comprehensive, coherent final summary."""),
        HumanMessage(content=f"""Please create a comprehensive final summary by synthesizing these section summaries from a document. Eliminate redundancy and create a flowing, coherent summary with the following structure:

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
        start_time = time.time()
        response = llm.invoke(messages)
        end_time = time.time()
        
        log_info(f"Final summary creation completed in {end_time - start_time:.2f} seconds")
        log_info(f"Final summary length: {len(response.content)} characters")
        
        return response.content
    except Exception as e:
        log_error(f"Error creating final summary: {str(e)}")
        return None

def process_document(text, llm, chunk_size=4000, chunk_overlap=500, 
                    progress_bar=None, status_text=None):
    """Process the entire document and generate summary with progress updates"""
    
    log_info("Starting document processing")
    
    # Single chunk processing
    if len(text) <= 15000:
        log_info("Processing as single chunk")
        
        if status_text:
            status_text.text("Generating summary...")
        if progress_bar:
            progress_bar.progress(75)
        
        summary = summarize_text_chunk(llm, text)
        
        if progress_bar:
            progress_bar.progress(100)
        
        log_info("Single chunk processing completed")
        return summary
    
    # Multi-chunk processing
    log_info("Processing as multiple chunks")
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    chunk_summaries = []
    
    # Process each chunk
    for i, chunk in enumerate(chunks):
        log_info(f"Processing chunk {i+1}/{len(chunks)}")
        
        if status_text:
            status_text.text(f"Processing section {i+1} of {len(chunks)}...")
        
        summary = summarize_text_chunk(llm, chunk, i+1)
        if summary:
            chunk_summaries.append(summary)
            log_info(f"Chunk {i+1} processed successfully")
        else:
            log_warning(f"Failed to process chunk {i+1}")
        
        if progress_bar:
            progress_bar.progress(25 + (i + 1) * 50 // len(chunks))
        
        time.sleep(1)  # Rate limiting
    
    # Create final summary
    if chunk_summaries:
        log_info("Creating final comprehensive summary")
        
        if status_text:
            status_text.text("Creating final comprehensive summary...")
        if progress_bar:
            progress_bar.progress(90)
        
        final_summary = create_final_summary(llm, chunk_summaries)
        
        if progress_bar:
            progress_bar.progress(100)
        
        log_info("Multi-chunk processing completed")
        return final_summary
    
    log_error("No chunk summaries generated")
    return None
