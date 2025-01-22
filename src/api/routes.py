from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from .utils import allowed_file, extract_text_from_pdf
from .config import UPLOAD_FOLDER

bp = Blueprint('main', __name__)

@bp.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            extracted_text = extract_text_from_pdf(filepath)
            os.remove(filepath)  # Clean up uploaded file
            return jsonify({'text': extracted_text})
        except Exception as e:
            os.remove(filepath)  # Clean up on error
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400
