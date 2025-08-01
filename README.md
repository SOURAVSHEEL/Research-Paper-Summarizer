# PDF Research Paper Summarizer - README

## Overview

A modular, AI-powered PDF summarizer application built with Streamlit and ChatGoogleGenerativeAI. This application allows users to upload research papers in PDF format and generates comprehensive, structured summaries using Google's Gemini AI model.

## Features

- 📄 **PDF Upload \& Processing**: Upload research papers and extract text automatically
- 🤖 **AI-Powered Summarization**: Uses ChatGoogleGenerativeAI (Gemini 2.0 Flash) for intelligent summarization
- 📊 **Smart Text Chunking**: Handles large documents by splitting them into manageable chunks
- 🎨 **Clean, Interactive UI**: Professional interface with progress tracking
- ⚙️ **Configurable Settings**: Adjustable chunk size and overlap parameters
- 💾 **Download Results**: Save summaries as text files
- 📈 **Compression Statistics**: View original vs. summary length metrics
- 🔄 **Modular Architecture**: Well-organized, maintainable codebase


## Project Structure

```
pdf_summarizer/
├── app.py                      # Main application entry point
├── modules/
│   ├── __init__.py
│   ├── document_processo.py        # text extraction and processing
│   ├── llm_handler.py          # ChatGoogleGenerativeAI integration
│   └── ui_components.py        # Streamlit UI components and styling
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Utility functions
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```


## Installation

### 1. Clone or Download the Repository

Create a new directory and save all the provided files in the correct structure.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```


### 3. Get Google API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create a free account
3. Generate an API key
4. **Optional**: Set as environment variable:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```


## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Application

1. **Enter API Key**: If not set as environment variable, enter your Google API key in the left panel
2. **Upload PDF**: Use the file uploader to select your research paper (PDF format)
3. **Adjust Settings** (Optional): Modify chunk size and overlap in the settings section
4. **Generate Summary**: Click "Generate Summary" to process your document
5. **Download Results**: Save the generated summary as a text file

### File Information Display

The left panel will show:

- Uploaded file name
- File size in bytes and MB
- Processing settings (chunk size, overlap)


### Summary Structure

Generated summaries include:

- **Title \& Authors**: Extracted publication information
- **Abstract/Overview**: Main research purpose and scope
- **Research Objectives**: Key questions and hypotheses
- **Methodology**: Research methods and approaches
- **Key Findings**: Main results and discoveries
- **Conclusions**: Primary conclusions and significance
- **Implications**: Broader impact and future directions
- **Limitations**: Noted limitations or areas for improvement


## Configuration

### Processing Settings

- **Chunk Size** (2000-6000 characters): Size of text sections for processing
- **Chunk Overlap** (200-1000 characters): Overlap between chunks for context preservation


### Model Configuration

The application uses:

- **Model**: `gemini-2.0-flash`
- **Temperature**: `0.2` (focused, consistent outputs)
- **Max Retries**: `3`


## API Limits (Free Tier)

Google's free tier includes:

- **Rate Limit**: 15 requests per minute
- **Daily Limit**: 200 requests per day
- **Token Limit**: 1 million tokens per minute

The application includes built-in rate limiting to prevent API errors.

## Troubleshooting

### Common Issues

1. **"Failed to initialize the AI model"**
    - Check your API key is correct
    - Verify internet connection
    - Ensure API key has proper permissions
2. **"Failed to extract text from PDF"**
    - Try a different PDF file
    - Ensure PDF contains readable text (not just images)
    - Check file isn't corrupted
3. **Processing Takes Too Long**
    - Large documents are processed in chunks
    - Processing time depends on document size
    - Free tier has rate limits that may slow processing

### File Size Recommendations

- **Optimal**: Under 10 MB
- **Maximum**: Up to 50 MB (may be slower)
- **Pages**: Works with documents of 100+ pages


## Technical Details

### Dependencies

- `streamlit`: Web application framework
- `langchain-google-genai`: Google Gemini integration
- `PyPDF2`: PDF text extraction
- `langchain-text-splitters`: Text chunking utilities
- `langchain-core`: Core LangChain functionality


### Performance Considerations

- **Memory Usage**: Efficient text chunking prevents memory overflow
- **Rate Limiting**: Built-in delays between API requests
- **Error Handling**: Comprehensive error management and recovery
- **Progress Tracking**: Real-time processing updates

## Development

### Adding New Features

The modular structure makes it easy to extend:

- **UI changes**: Modify `modules/ui_components.py`
- **PDF processing**: Update `modules/pdf_processor.py`
- **AI integration**: Enhance `modules/llm_handler.py`
- **Utilities**: Add helpers in `utils/helpers.py`

### Testing

Test the application with various PDF types:

- Academic papers
- Technical documents
- Multi-page reports
- Different file sizes