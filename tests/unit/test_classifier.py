import pytest
from datetime import datetime
import numpy as np
from src.models.extracted_document import ExtractedDoc
from src.services.document_classifier import DocumentClassifier
from src.models.classified_document import ClassifiedDoc
from src.config import config
from datetime import datetime


@pytest.fixture
def classifier():
    return DocumentClassifier()


@pytest.fixture
def mock_data():
    invoice_text = """Company Name Customer Company Name Address Contact Name Phone Address Email Phone Website Email Invoice Number: 1234 Issue Date: Date Expiry Date: Date Item Description Quantity Unit Price Total Subtotal TOTAL"""
    bank_statement_text = """Bank 1 of Testing\nCustomer Support: 1-800-555-1234\nwww.fakebankdomain.com\nAccount Holder: John Doe 1\nAccount Number: XXXX-XXXX-XXXX-6781\nStatement Period: 2023-01\nDate Description Debit ($) Credit ($)\n01/01/2023 Direct Deposit 326.73\n20/01/2023 Direct Deposit 424.61\n04/01/2023 ACH Payment 215.70\n03/01/2023 Check Deposit 464.84\n20/01/2023 Debit Card Purchase 695.38\n04/01/2023 POS Purchase 136.10\n27/01/2023 Online Transfer 285.34\n05/01/2023 ACH Payment 436.96\n16/01/2023 POS Purchase 203.32\n15/01/2023 POS Purchase 613.07\n28/01/2023 POS Purchase 189.97\n07/01/2023 Debit Card Purchase 65.51\n08/01/2023 Check Deposit 592.13\n20/01/2023 Debit Card Purchase 289.50\n28/01/2023 POS Purchase 10.44\n24/01/2023 Loan Repayment 541.03\nBank 1 - Confidential Statement | Page 1Bank 1 of Testing\nCustomer Support: 1-800-555-1234\nwww.fakebankdomain.com\nEnd of Statement\nBank 1 - Confidential Statement | Page 2"""
    drivers_license_text = """HAWAIL LICENSE NUMBER Q4-47-87441 196 Peace 06/03/2008 EYES Samx CTY M0 ISSUE DA 06/18/1998 TO Wie pe wom ST HONOLULU, HI 96820"""

    return {
        "invoice": ExtractedDoc("invoice.pdf", invoice_text, datetime.now()),
        "bank_statement": ExtractedDoc("bank_statement.pdf", bank_statement_text, datetime.now()),
        "drivers_license": ExtractedDoc("drivers_license.pdf", drivers_license_text, datetime.now()),
        "unknown": ExtractedDoc("unknown.pdf", "unknown", datetime.now()),
    }


def test_invoice_classification(classifier, mock_data):
    """Test that invoice documents are correctly classified"""
    response = classifier.classify_document(mock_data["invoice"])
    assert response.file_type == "invoice"
    assert response.confidence > config.CONFIDENCE_THRESHOLD


def test_bank_statement_classification(classifier, mock_data):
    """Test that bank statements are correctly classified"""
    response = classifier.classify_document(mock_data["bank_statement"])
    assert response.file_type == "bank_statement"
    assert response.confidence > config.CONFIDENCE_THRESHOLD


def test_drivers_license_classification(classifier, mock_data):
    """Test that driver's licenses are correctly classified"""
    response = classifier.classify_document(mock_data["drivers_license"])
    assert response.file_type == "drivers_license"
    assert response.confidence > config.CONFIDENCE_THRESHOLD


def test_unknown_document_classification(classifier, mock_data):
    """Test that unknown documents are correctly handled"""
    response = classifier.classify_document(mock_data["unknown"])
    assert response.file_type == "unknown"
    assert response.confidence < config.CONFIDENCE_THRESHOLD


def test_empty_document_handling(classifier):
    """Test handling of empty documents"""
    empty_doc = ExtractedDoc("empty.pdf", "", datetime.now())
    response = classifier.classify_document(empty_doc)
    assert response.file_type == "unknown"
    assert response.confidence < config.CONFIDENCE_THRESHOLD


def test_compute_similarity(classifier):
    """Test the similarity computation function"""
    embedding1 = np.array([1, 0, 0])
    embedding2 = np.array([1, 0, 0])
    similarity = classifier.compute_similarity(embedding1, embedding2)
    assert similarity == pytest.approx(1.0)

    embedding1 = np.array([1, 0, 0])
    embedding2 = np.array([0, 1, 0])
    similarity = classifier.compute_similarity(embedding1, embedding2)
    assert similarity == pytest.approx(0.0)


def test_multiple_classifications(classifier, mock_data):
    """Test that classifier gives consistent results for multiple runs"""
    results = []
    for _ in range(3):
        response = classifier.classify_document(mock_data["invoice"])
        results.append((response.file_type, response.confidence))

    assert all(result[0] == results[0][0] for result in results)  # Same document type
    assert all(abs(result[1] - results[0][1]) < 1e-6 for result in results)  # Same confidence


def test_response_structure(classifier, mock_data):
    """Test that response has all required fields"""
    response = classifier.classify_document(mock_data["invoice"])
    assert isinstance(response, ClassifiedDoc)
    assert hasattr(response, 'file_name')
    assert hasattr(response, 'file_type')
    assert hasattr(response, 'confidence')
    assert hasattr(response, 'processed_at')
    assert hasattr(response, 'text_content')
    assert hasattr(response, 'classified_at')