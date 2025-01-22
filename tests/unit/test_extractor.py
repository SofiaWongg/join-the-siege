import pytest
from datetime import datetime
from io import BytesIO
from src.services.document_extractor import Extractor
from werkzeug.datastructures import FileStorage


@pytest.fixture
def extractor():
    return Extractor()


@pytest.fixture
def sample_pdf_content():
    # Sample invoice content
    return """INVOICE Company Name Customer Company Name 
    Address Contact Name Phone Address Email Phone Website 
    Email Invoice Number: 1234 Issue Date: Date 
    Expiry Date: Date Item Description Quantity Unit Price 
    Total Subtotal Tax TOTAL"""


@pytest.fixture
def mock_pdf_file(sample_pdf_content):
    return FileStorage(
        stream=BytesIO(sample_pdf_content.encode("utf-8")),
        filename="test_invoice.pdf",
        content_type="application/pdf",
    )


@pytest.fixture
def mock_empty_file():
    return FileStorage(
        stream=BytesIO(b""), filename="empty.pdf", content_type="application/pdf"
    )


def test_extract_text_pdf(extractor, mock_pdf_file, mocker):
    """Test PDF text extraction with mock PDF"""
    # Setup the mock
    mock_page = mocker.MagicMock()
    mock_page.extract_text.return_value = """INVOICE Company Name Customer Company Name 
    Address Contact Name Phone Address Email Phone Website 
    Email Invoice Number: 1234 Issue Date: Date"""

    mock_pdf = mocker.MagicMock()
    mock_pdf.pages = [mock_page]
    mock_pdf.__enter__.return_value = mock_pdf

    mocker.patch("pdfplumber.open", return_value=mock_pdf)

    # Run the function
    extracted_text = extractor.extract_text_pdf(mock_pdf_file)

    # Assertions
    assert extracted_text is not None
    assert "Invoice" in extracted_text
    assert "Number" in extracted_text


def test_extract_text_pdf_with_empty_file(extractor, mock_empty_file):
    """Test PDF extraction with empty file"""
    extracted_text = extractor.extract_text_pdf(mock_empty_file)
    assert extracted_text == ""


def test_process_document_pdf(extractor, mock_pdf_file, mocker):
    """Test complete document processing for PDF"""
    # Mock the extract_text_pdf method
    mocker.patch.object(
        extractor, "extract_text_pdf", return_value="Invoice test content"
    )

    result = extractor.process_document(mock_pdf_file)
    assert result.file_path == "test_invoice.pdf"
    assert "Invoice test content" in result.extracted_text
    assert isinstance(result.processed_at, datetime)


def test_process_document_image(extractor, mocker):
    """Test processing of image files"""
    # Create mock image file
    image_file = FileStorage(
        stream=BytesIO(b"fake image content"),
        filename="test.jpg",
        content_type="image/jpeg",
    )

    # Mock image extraction
    mocker.patch.object(
        extractor, "extract_text_image", return_value="Image extracted text"
    )

    result = extractor.process_document(image_file)
    assert result.file_path == "test.jpg"
    assert "Image extracted text" in result.extracted_text
    assert isinstance(result.processed_at, datetime)


def test_process_document_unsupported_file(extractor):
    """Test handling of unsupported file types"""
    unsupported_file = FileStorage(
        stream=BytesIO(b"unsupported content"),
        filename="test.txt",
        content_type="text/plain",
    )

    result = extractor.process_document(unsupported_file)
    assert result.file_path == "test.txt"
    assert (
        result.extracted_text == ""
    )  # Should return empty string for unsupported files


def test_process_document_error_handling(extractor, mock_pdf_file, mocker):
    """Test error handling during document processing"""
    # Mock extract_text_pdf to raise an exception
    mocker.patch.object(
        extractor, "extract_text_pdf", side_effect=Exception("Test error")
    )

    result = extractor.process_document(mock_pdf_file)
    assert result.file_path == "test_invoice.pdf"
    assert result.extracted_text == ""  # Should return empty string on error


def test_extract_text_pdf_filter_short_words(extractor, mock_pdf_file, mocker):
    """Test that words shorter than 2 characters are filtered"""
    test_text = "a an the big cats"

    mock_page = mocker.MagicMock()
    mock_page.extract_text.return_value = test_text

    mock_pdf = mocker.MagicMock()
    mock_pdf.pages = [mock_page]
    mock_pdf.__enter__.return_value = mock_pdf

    mocker.patch("pdfplumber.open", return_value=mock_pdf)

    extracted_text = extractor.extract_text_pdf(mock_pdf_file)
    assert "an" not in extracted_text.lower()
    assert "big" in extracted_text
    assert "cats" in extracted_text
