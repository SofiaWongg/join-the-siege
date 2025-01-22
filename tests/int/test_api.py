import pytest
from src.app import app
from io import BytesIO
from src.services.document_classifier import DocumentClassifier
from src.services.document_extractor import Extractor
from src.models.extracted_document import ExtractedDoc
from src.models.classified_document import ClassifiedDoc
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_no_file_in_request(client):
    response = client.post('/classify_file')
    assert response.status_code == 400

def test_no_selected_file(client):
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400

def test_success(client, mocker):
    mock_doc_info = ExtractedDoc(
        file_path='test.pdf',
        extracted_text='test content',
        processed_at=datetime.now()
    )
    
    mocker.patch.object(
        Extractor,
        'process_document',
        return_value=mock_doc_info
    )

    mock_response = ClassifiedDoc(
        file_name='test.pdf',
        file_type='invoice',
        confidence=0.95,
        processed_at=datetime.now(),
        text_content='test content',
        classified_at=datetime.now()
    )
    
    mocker.patch.object(
        DocumentClassifier,
        'classify_document',
        return_value=mock_response
    )

    data = {'file': (BytesIO(b"dummy content"), 'file.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'file_type' in json_data
    assert 'confidence' in json_data
    assert json_data['file_type'] == 'invoice'
    assert json_data['confidence'] == 0.95

def test_multiple_files(client):
    """Test that sending multiple files returns 400"""
    data = {
        'file1': (BytesIO(b"content1"), 'file1.pdf'),
        'file2': (BytesIO(b"content2"), 'file2.pdf')
    }
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_invoice_flow(client):
    """Test the PDF flow"""
    # Read the actual invoice content
    with open('files/invoice_2.pdf', 'rb') as f:
        pdf_content = f.read()
    
    data = {
        'file': (BytesIO(pdf_content), 'invoice.pdf', 'application/pdf')
    }
    
    response = client.post('/classify_file', data=data)
    
    assert response.status_code == 200
    result = response.json
    assert result['file_type'] == 'invoice'
    assert result['confidence'] > 0.25

def test_image_flow(client):
    """Test the image flow"""
    # Read the actual invoice content
    with open('files/drivers_license_1.jpg', 'rb') as f:
        image_content = f.read()

    data = {
        'file': (BytesIO(image_content), 'drivers_license_1.jpg', 'image/jpeg')
    }
    
    response = client.post('/classify_file', data=data)
    
    assert response.status_code == 200
    result = response.json
    assert result['file_type'] == 'drivers_license'
    assert result['confidence'] > 0.25 

def test_no_type_pdf_flow(client):
    """Test the PDF flow for a doc with no type"""
    # Read the actual invoice content
    with open('files/no_type.pdf', 'rb') as f:
        pdf_content = f.read()
    
    data = {
        'file': (BytesIO(pdf_content), 'no_type.pdf', 'application/pdf')
    }
    
    response = client.post('/classify_file', data=data)
    
    assert response.status_code == 200
    result = response.json
    assert result['file_type'] == 'unknown'
    assert result['confidence'] < 0.25

def test_batch_no_files(client):
    """Test that sending no files returns 400"""
    response = client.post('/classify_files')
    assert response.status_code == 400

def test_batch_success(client):
    """Test successful batch processing"""
    # Create test files - note the changed data structure
    data = {
        'files[]': [
            (BytesIO(b"dummy content 1"), 'file1.pdf'),
            (BytesIO(b"dummy content 2"), 'file2.pdf')
        ]
    }
    
    response = client.post(
        '/classify_files',
        data=data,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    result = response.get_json()
    assert 'processed' in result
    assert 'results' in result
    assert result['processed'] == 2
    assert len(result['results']) == 2

def test_batch_mixed_success(client):
    """Test batch processing with some failures"""
    data = {
        'files[]': [
            (BytesIO(b"valid content"), 'valid.pdf'),
            (BytesIO(b"bad content"), 'invalid.xyz')
        ]
    }
    
    response = client.post(
        '/classify_files',
        data=data,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    result = response.get_json()
    assert result['processed'] == 2
    assert len(result['results']) == 2
    # One success, one error
    assert any('error' in r for r in result['results'])