# QuizTonic API – Retrieval-Augmented Quiz Automated Maker

QuizTonic API is an AI-powered backend service designed to generate quizzes from any type of content, including documents, videos, and more. Leveraging state-of-the-art retrieval and language generation techniques, QuizTonic API allows applications to quickly create engaging and informative quizzes, seamlessly blending content understanding with automation.

## 🚀 Features

- **Multi-format Content Support**: Generate quizzes from text content, PDF files, web pages, YouTube videos, and video files
- **Intelligent Content Processing**: Advanced text chunking and vector embeddings for optimal content understanding
- **Flexible Quiz Generation**: Customizable number of questions and answer choices
- **Flashcard Generation**: Create study flashcards alongside quizzes
- **Cost Tracking**: Real-time monitoring of API usage and costs
- **Web Interface**: User-friendly sandbox for testing and configuration
- **AWS Lambda Ready**: Deployable as serverless function with CORS support

## 🛠️ Technology Stack

### Core AI & ML Technologies

#### **RAG (Retrieval-Augmented Generation)**
- **Purpose**: Combines information retrieval with text generation to create contextually accurate content
- **Implementation**: QuizTonic API uses RAG to retrieve relevant content chunks before generating quiz questions
- **Benefits**: Ensures questions are based on actual content rather than hallucinated information

#### **Vector Embeddings & Semantic Search**
- **Technology**: OpenAI's `text-embedding-3-small` model
- **Purpose**: Converts text chunks into high-dimensional vectors for semantic similarity search
- **Why it matters**: Enables finding relevant content based on meaning, not just keyword matching
- **Performance**: 1536-dimensional vectors optimized for speed and accuracy

#### **FAISS (Facebook AI Similarity Search)**
- **Purpose**: High-performance vector database for similarity search and clustering
- **Role in QuizTonic API**: Stores and efficiently searches through content embeddings
- **Benefits**: Fast retrieval of relevant content chunks for quiz generation
- **Scalability**: Handles large document collections with sub-second search times

#### **OpenAI GPT Models**
- **Primary Model**: `gpt-4o-mini` for quiz generation
- **Purpose**: Large Language Model for generating questions, answers, and explanations
- **Cost Optimization**: Uses efficient model for production while maintaining quality
- **Customization**: Specialized prompts for different question types and difficulty levels

#### **LangChain Framework**
- **Purpose**: AI orchestration framework that connects and manages all AI components
- **Components Used**:
  - `langchain-core`: Prompt templates and structured output
  - `langchain-openai`: OpenAI model integration (GPT + Embeddings)
  - `langchain-community`: FAISS vector store integration
  - `langchain-text-splitters`: Intelligent text chunking
- **Benefits**: Simplified API management, automatic validation, error handling, and seamless integration between AI services
- **Role**: Acts as the "conductor" orchestrating the entire AI generation pipeline

### Backend & Infrastructure

#### **Python 3.9+**
- **Framework**: Core application language
- **Libraries**: Extensive ecosystem for AI/ML, web scraping, and document processing
- **Performance**: Optimized for data processing and API development

#### **Flask**
- **Purpose**: Lightweight web framework for API development
- **Features**: RESTful API endpoints, request handling, and response formatting
- **Flexibility**: Easy to extend and customize for different deployment scenarios

#### **AWS Lambda**
- **Purpose**: Serverless computing platform for scalable deployment
- **Benefits**: Automatic scaling, pay-per-use pricing, and zero server management
- **Integration**: Seamless deployment with Docker containers

#### **Docker**
- **Purpose**: Containerization for consistent deployment across environments
- **Benefits**: Reproducible builds, easy scaling, and environment isolation
- **Deployment**: Enables seamless migration between local development and cloud production

### Document Processing & Content Extraction

#### **PyMuPDF (fitz)**
- **Purpose**: PDF text extraction and document processing
- **Features**: High-quality text extraction, metadata handling, and image processing
- **Performance**: Fast processing of large PDF documents

#### **BeautifulSoup4**
- **Purpose**: Web scraping and HTML/XML parsing
- **Features**: Robust parsing of web content, handling malformed HTML
- **Integration**: Works with requests library for complete web scraping solution

#### **Pydantic**
- **Purpose**: Data validation and serialization using Python type annotations
- **Benefits**: Automatic data validation, clear error messages, and type safety
- **Usage**: Defines quiz models, API schemas, and configuration structures

### Data Processing & Storage

#### **Text Chunking & Preprocessing**
- **Algorithm**: Sliding window approach with configurable overlap
- **Purpose**: Breaks large documents into manageable pieces for processing
- **Optimization**: Balances context preservation with processing efficiency

#### **Language Detection**
- **Library**: Custom implementation for multi-language support
- **Purpose**: Automatically detects content language for localized quiz generation
- **Features**: Supports multiple languages with appropriate prompt templates

### Web & Frontend Technologies

#### **HTML5 & CSS3**
- **Purpose**: Web interface for testing and configuration
- **Features**: Responsive design, modern styling, and user-friendly interface
- **Integration**: Works seamlessly with Flask templating system

#### **JavaScript (Vanilla)**
- **Purpose**: Frontend interactivity and API communication
- **Features**: Dynamic form handling, real-time feedback, and error management
- **Simplicity**: No complex frameworks for easy maintenance and deployment

### Development & Deployment Tools

#### **Git & GitHub**
- **Purpose**: Version control and collaborative development
- **Features**: Branch management, pull requests, and issue tracking

#### **Docker Compose** (Optional)
- **Purpose**: Local development environment orchestration
- **Benefits**: Easy setup of complex multi-service applications

#### **Shell Scripts**
- **Purpose**: Automation of deployment and setup processes
- **Files**: `setup_local.sh`, `deploy_lambda_url.sh`
- **Benefits**: Consistent environment setup and one-click deployment

### Monitoring & Analytics

#### **Cost Tracking**
- **Implementation**: Custom token counting and cost calculation
- **Purpose**: Monitor OpenAI API usage and associated costs
- **Features**: Real-time cost estimation and usage analytics

#### **Error Handling**
- **Framework**: Custom exception hierarchy
- **Purpose**: Graceful error handling and detailed logging
- **Benefits**: Easy debugging and user-friendly error messages

## 🏗️ Architecture

### Core Components

1. **QuizGenerator** (`src/raqam.py`): Main orchestrator that handles content processing and quiz generation
2. **Document Processing** (`src/document.py`): Text chunking and preprocessing
3. **Vector Store** (`src/vector_store.py`): FAISS-based semantic search and retrieval
4. **Content Sources**:
   - `src/pdf.py`: PDF text extraction using PyMuPDF
   - `src/web_page.py`: Web scraping with BeautifulSoup
5. **Quiz Models** (`src/quiz.py`): Pydantic schemas for questions and flashcards
6. **API Layer**: Flask web API and AWS Lambda handler

### Data Flow

```
Content Input → Document Processing → Vector Embeddings → Retrieval → LLM Generation → Quiz Output
```

## 📁 Project Structure

```
quiztonic_api/
├── api/                          # API layer
│   ├── api.py                   # Flask web server
│   ├── lambda_function.py       # AWS Lambda handler
│   ├── static/                  # Web interface assets
│   │   ├── script.js           # Frontend JavaScript
│   │   └── style.css           # Styling
│   └── templates/              # HTML templates
│       └── quiz_sandbox.html   # Web interface
├── src/                         # Core application logic
│   ├── raqam.py                 # Main QuizGenerator class
│   ├── language_detection.py    # Language detection and localization
│   ├── document.py             # Text document processing
│   ├── vector_store.py         # FAISS vector store
│   ├── quiz.py                 # Quiz and flashcard models
│   ├── quiz_config.py          # Configuration management
│   ├── pdf.py                  # PDF processing (pypdf)
│   ├── web_page.py             # Web scraping
│   ├── templates.py             # Legacy templates (obsolete)
│   ├── utils.py                # Utility functions
│   └── exception.py            # Custom exceptions
├── config/                      # Configuration files
│   └── default_config.yaml     # Default settings
├── deploy_lambda_url.sh         # AWS Lambda deployment script
├── setup_local.sh              # Local environment setup
├── test_lambda_url.py          # Test script for Lambda Function URL
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── API_CONTRACT.md             # API contract documentation
└── README.md                   # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9+
- OpenAI API key
- (Optional) AWS account for Lambda deployment

### Local Development

1. **Set up the development environment**:
```bash
cd quiztonic_api
chmod +x setup_local.sh
./setup_local.sh
```

2. **Activate the virtual environment**:
```bash
source venv/bin/activate
```

3. **Set up environment variables**:
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

4. **Run the Flask development server**:
```bash
python api/api.py
```

5. **Access the web interface**:
   - Open `http://localhost:5050/quiz-sandbox` in your browser

### AWS Lambda Deployment

1. **Build the container**:
```bash
docker build -t quiztonic-api-lambda .
```

2. **Deploy to AWS Lambda** using the provided Dockerfile and deployment script:
```bash
./deploy_lambda_url.sh
```

## 🔧 Configuration

### Default Settings (`config/default_config.yaml`)

```yaml
base_quiz_config: 
  model_name: "gpt-4o-mini"                    # LLM model
  embdeddings_model_name: "text-embedding-3-small"  # Embedding model
  embedding_batch_size: 10                    # Batch size for embeddings
  min_text_length: 500                        # Minimum content length
  chunk_size: 2000                           # Text chunk size
  chunk_overlap: 100                         # Chunk overlap
  local_vector_store_path: null              # Vector store persistence
```

### Supported Content Sources

- **Text Content**: Direct text input
- **PDF Files**: Upload and process PDF documents
- **Web Pages**: Extract content from URLs
- **YouTube Videos**: Process video transcripts (planned)
- **Video Files**: Extract audio transcripts (planned)

## 📡 API Endpoints

### Flask API (`api/api.py`)

- `POST /generate-quiz`: Generate quiz from content
- `GET /quiz-sandbox`: Web interface
- `GET /get-config`: Retrieve current configuration
- `GET /get-default-config`: Get default settings
- `POST /set-custom-config`: Update configuration

### AWS Lambda Function URL

The API is deployed as an AWS Lambda Function URL for serverless access. See `API_CONTRACT.md` for detailed API documentation.

## 🧠 How It Works

### 1. Content Processing
- Input content is processed and chunked into manageable pieces
- Text is cleaned and preprocessed for optimal processing

### 2. Vector Embeddings
- Content chunks are converted to vector embeddings using OpenAI's embedding models
- FAISS vector store enables semantic search and retrieval

### 3. Intelligent Retrieval
- Relevant content chunks are retrieved based on the quiz generation query
- Ensures questions are generated from the most relevant parts of the content

### 4. LLM Generation
- Retrieved content is fed to GPT models with specialized prompts
- Generates multiple-choice questions with explanations
- Creates flashcards for key concepts

### 5. Output Processing
- Questions are randomized to prevent pattern recognition
- Answer choices are shuffled while maintaining correct answer mapping
- Cost and token usage are tracked and reported

## 💰 Cost Management

The system tracks and reports:
- **Input tokens**: Text sent to the LLM
- **Output tokens**: Generated responses
- **Embedding tokens**: Vector embeddings
- **Estimated costs**: Based on OpenAI pricing

## 🔒 Error Handling

Custom exception hierarchy:
- `RAQAMException`: Base exception class
- `InvalidInputDataException`: Invalid input validation
- `DocumentParsingException`: Content processing errors
- `QuizGenerationException`: Quiz generation failures
- `FlashcardsGenerationException`: Flashcard generation errors
- `WebPageException`: Web scraping errors

## 🚀 Deployment Options

### 1. Local Flask Server
- Development and testing
- Full web interface available
- Easy debugging and configuration

### 2. AWS Lambda
- Serverless deployment
- Automatic scaling
- Cost-effective for production
- CORS support for web applications

### 3. Docker Container
- Consistent deployment environment
- Easy integration with existing infrastructure

## 🔧 Customization

### Prompt Templates
Modify `src/templates.py` to customize:
- Question generation prompts
- Flashcard generation prompts
- Retrieval queries

### Configuration
- Adjust chunk sizes for different content types
- Modify embedding batch sizes for performance optimization
- Configure vector store persistence for faster subsequent runs

## 📊 Performance Considerations

- **Chunk Size**: Larger chunks provide more context but increase processing time
- **Batch Size**: Optimize embedding batch size based on available memory
- **Vector Store**: Persist vector stores to avoid re-computing embeddings
- **Model Selection**: Balance between cost and quality (GPT-4o-mini vs GPT-4)

## 📚 API Documentation

See `API_CONTRACT.md` for detailed API documentation including:
- Request/Response formats
- Error handling
- Versioning
- Rate limiting
- Authentication (if applicable)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- **QuizTonic Mobile App**: [https://github.com/Bptmn/quiztonic](https://github.com/Bptmn/quiztonic)
  - Flutter application that consumes this API
  - Available on iOS and Android

## 🆘 Support

For issues and questions:
1. Check the error logs for detailed stack traces
2. Verify your OpenAI API key is valid
3. Ensure input content meets minimum length requirements
4. Check network connectivity for web scraping features
5. Review `API_CONTRACT.md` for API usage guidelines
