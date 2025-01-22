from flask import Blueprint, request, jsonify
from src.services.document_classifier import DocumentClassifier
from src.services.document_extractor import Extractor
from src.utils.valid_types import is_allowed_file
import os
import logging
from werkzeug.exceptions import RequestEntityTooLarge

api = Blueprint("api", __name__)

HTTP_ERRORS = {
    "file_required": ("No file provided", 400),
    "file_type": ("File type not allowed", 415),
    "file_too_large": ("File exceeds size limit", 413),
    "processing_error": ("Error processing document", 500),
}


def error_response(error_key):
    message, status_code = HTTP_ERRORS[error_key]
    return jsonify({"error": message}), status_code


@api.route("/classify_file", methods=["POST"])
def classify_file_route():
    logging.info("Classify file route called")

    try:
        if "file" not in request.files:
            logging.error("No file part in the request")
            return error_response("file_required")

        file = request.files["file"]
        if file.filename == "":
            logging.error("No selected file")
            return error_response("file_required")

        if not is_allowed_file(file.filename):
            logging.error(f"File type not allowed: {file.filename}")
            return error_response("file_type")

        try:
            extractor = Extractor()
            classifier = DocumentClassifier()

            doc_info = extractor.process_document(file)
            response = classifier.classify_document(doc_info)

            return jsonify(response.to_dict()), 200

        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {str(e)}")
            return error_response("processing_error")

    except RequestEntityTooLarge:
        return error_response("file_too_large")
    except Exception as e:
        logging.error(f"Unexpected error processing file: {str(e)}")
        return error_response("processing_error")
