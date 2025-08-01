# Document Summarizer

A powerful, modular AI-powered document summarizer application built with Streamlit and Google's Gemini AI. This application supports multiple file formats and provides intelligent summarization with a clean, user-friendly interface.

## 🚀 Features

### **Document Processing**

- 📄 **Multi-format Support**: PDF, DOCX, DOC, TXT, and Markdown files
- 🔍 **Smart Text Extraction**: Intelligent text extraction for each format
- 📊 **Document Analytics**: File size, page count, and processing statistics
- 🔧 **Configurable Processing**: Adjustable chunk sizes and overlap settings


### **AI-Powered Summarization**

- 🤖 **Google Gemini Integration**: Uses ChatGoogleGenerativeAI (Gemini 2.0 Flash)
- 📋 **Structured Summaries**: Organized sections with key insights
- 🎯 **Comprehensive Analysis**: Objectives, methodology, findings, and implications
- 🔄 **Intelligent Chunking**: Handles large documents efficiently


### **User Interface**

- 🎨 **Modern Design**: Clean, professional interface with Inter font
- 📊 **Real-time Progress**: Processing status with progress indicators
- 💾 **Export Options**: Download summaries as text files


## 📁 Project Structure

```
document_summarizer/
├── app.py                      # Main application entry point
├── modules/
│   ├── __init__.py
│   ├── document_processor.py   # Multi-format document processing
│   ├── llm_handler.py          # ChatGoogleGenerativeAI integration
│   └── ui_components.py        # Streamlit UI components
├── utils/
│   ├── __init__.py
│   ├── helpers.py              # Utility functions
│   └── logger.py               # Logging configuration
├── logs/                       # Daily log files directory
│   └── .gitkeep
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```


## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Google API key for Gemini AI


### Step 1: Clone/Download the Project

```bash
git clone <repository-url>
cd document_summarizer
```


### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```


### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```


### Step 4: Create Environment File

Create a `.env` file in the project root:

```env
# Environment Variables
GOOGLE_API_KEY=your_google_api_key_here
```


### Step 5: Get Google API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Document Summarizer

1. **Upload Document**
    - Click "📁 Settings" to show the sidebar (if hidden)
    - Use the file uploader to select your document
    - Supported formats: PDF, DOCX, DOC, TXT, MD
2. **Configure Settings** (Optional)
    - Adjust chunk size (2000-6000 characters)
    - Set chunk overlap (200-1000 characters)
    - These settings affect how large documents are processed
3. **Generate Summary**
    - Click "🚀 Generate Summary"
    - Monitor progress with the status indicators
    - View the structured summary when complete
4. **Export Results**
    - Click "💾 Download Summary" to save as text file
    - View analytics (compression ratio, reading time)
    - Generate new summaries as needed

### Sidebar Control

- **Show Sidebar**: Click "📁 Settings" button
- **Hide Sidebar**: Click "❌ Hide" button
- **Full Screen**: Hide sidebar for maximum document viewing space


## 📋 Summary Structure

Generated summaries include:

- **Title \& Authors**: Document title and author information
- **Abstract/Overview**: Main purpose and scope
- **Research Objectives**: Key questions and hypotheses
- **Methodology**: Research methods and approaches
- **Key Findings**: Main results and discoveries
- **Conclusions**: Primary conclusions and significance
- **Implications**: Future directions and broader impact
- **Limitations**: Noted limitations or areas for improvement


## ⚙️ Configuration

### Environment Variables

```env
GOOGLE_API_KEY=your_api_key_here
```


### Processing Settings

- **Chunk Size**: 2000-6000 characters (default: 4000)
- **Chunk Overlap**: 200-1000 characters (default: 500)
- **Model**: Gemini 2.0 Flash
- **Temperature**: 0.2 (focused responses)


### Supported File Types

- **PDF**: Research papers, reports, articles
- **DOCX/DOC**: Microsoft Word documents
- **TXT**: Plain text files
- **MD**: Markdown files with formatting


## 📊 Performance

### API Limits (Free Tier)

- **Rate Limit**: 15 requests per minute
- **Daily Limit**: 200 requests per day
- **Token Limit**: 1 million tokens per minute

### Processing Capabilities

- **Single Documents**: Up to 15,000 characters processed as one chunk
- **Large Documents**: Automatically chunked for efficient processing
- **File Sizes**: Supports documents up to 50MB
- **Page Limits**: Handles 100+ page documents


## 📝 Logging

### Log Files

- **Location**: `logs/` directory
- **Format**: `document_summarizer_YYYYMMDD.log`
- **Content**: Processing steps, errors, performance metrics
- **Rotation**: Daily log files

### Log Levels

- **INFO**: Normal operations, processing steps
- **WARNING**: Non-critical issues
- **ERROR**: Processing failures, API errors


## 🔧 Troubleshooting

### Common Issues

**"Failed to initialize the AI model"**

- Check your API key in `.env` file
- Verify internet connection
- Ensure API key has proper permissions

**"Failed to extract text from document"**

- Try a different document file
- Ensure document contains readable text
- Check file isn't corrupted or password-protected

**"Processing takes too long"**

- Large documents are processed in chunks
- Free tier has rate limits (15 requests/minute)
- Consider breaking very large documents into smaller parts

### File Upload Issues

- Check file format is supported
- Ensure file size is reasonable (< 50MB)
- Try different encoding for text files
- Verify file isn't corrupted

### Development Setup

1. Fork the repository
2. Create virtual environment
3. Install dependencies
4. Create `.env` with your API key
5. Make changes and test
6. Submit pull request

### Code Structure

- **Modular Design**: Separated concerns across modules
- **Clean UI**: Modern, responsive interface
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed operation tracking

**Happy Summarizing! 📄✨**

