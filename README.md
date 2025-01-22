# Document Classifier

A Flask API that classifies documents (PDFs, images) into categories like invoices, bank statements, and driver's licenses using their embeddings.

## Features

- Document text extraction from PDFs and images
- ML-based document classification
- Unit & Integration Tests

## Getting Started

### Prerequisites

- Python 3.11
- tesseract-ocr

### Installation

1. Clone the repository

```bash
git clone https://github.com/SofiaWongg/join-the-siege.git
```

2.Create and activate virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python -m src.app
```

## Usage

### Classify a single file
POST /classify_file
### Request
{
    "file": (File, "path/to/file.pdf")
}

example:
```bash
curl -X POST -F 'file=@/Users/sofiawong/Desktop/join-the-siege/files/drivers_license_1.jpg' http://127.0.0.1:5000/classify_file
```

### Response
{
    "file_name": "example.pdf",
    "file_type": "invoice",
    "confidence": 0.85,
    "processed_at": "2025-01-21T10:30:00",
    "text_content": "extracted text...",
    "classified_at": "2025-01-21T10:30:01"
}

### Batch classify multiple files
POST /classify_files
#Request
{
    "file": (File, "path/to/file.pdf")
}

example:
```bash
curl -X POST -F 'files[]=@/Users/sofiawong/Desktop/join-the-siege/files/drivers_license_1.jpg' -F 'files[]=@/Users/sofiawong/Desktop/join-the-siege/files/invoice_2.pdf' http://127.0.0.1:5000/classify_files
```

### Response
```
{
    "processed": 2,
    "results": [
        {
            "file_name": "example.pdf",
            "file_type": "invoice",
            "confidence": 0.85,
            "processed_at": "2025-01-21T10:30:00",
            "text_content": "extracted text...",
            "classified_at": "2025-01-21T10:30:01"
        },
        {
            "file_name": "example.pdf",
            "file_type": "drivers_license",
            "confidence": 0.95,
            "processed_at": "2025-01-21T10:30:00",
            "text_content": "extracted text...",
            "classified_at": "2025-01-21T10:30:01"
        }
    ]
}
```

## Error Responses


400: No file provided

415: Unsupported file type

413: File too large

500: Processing error

## Testing
Run the tests:
```bash
pytest
```

## Solution Overview
### Architecture


### Document Extractor:

Extracts text from PDFs and images
Processes and cleans extracted text


### Document Classifier:

Uses sentence transformers for document embedding
Compares document embeddings with reference text embeddings
Returns document type and confidence score


### API Layer:

Handles HTTP requests/responses
Manages error handling and logging
Provides clear status codes and error messages

## Improvements
### Functionality
Content-based classification - not dependant on filename \
Confidence scoring for better handling of edge cases 

### Scalability
Organized folder structure (tests, services, models, api) \
Easy industry expansion via config file reference types \
Batch processing capabilities 

### Maintainability
Modular architecture for better testing and reuse \
Centralized configuration \
Logging for debugging 

## Future Work

### Features

Enhanced text extraction for complex layouts \
NER integration for improved embeddings \
Multi-factor classification (embeddings + keywords + metadata) \
Additional document type support \
Enhanced error handling \
Improved input validation \
Extended test coverage


### Infrastructure

Docker containerization \
CI/CD pipeline \
Monitoring and alerting 

### Performance

Document caching \
Async processing for large files 
