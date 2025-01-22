from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Tuple
from src.models.extracted_document import ExtractedDoc
import logging
from src.config import config
from src.models.classified_document import ClassifiedDoc
from datetime import datetime


class DocumentClassifier:
    """classify documents with local lm model using embeddings"""

    def __init__(self):
        logging.info("Starting classifier")
        self.model = SentenceTransformer(config.MODEL_NAME)

        self.reference_texts: dict[str, str] = config.REFERENCE_TEXTS

        self.reference_embeddings: dict[str, np.ndarray] = {
            doc_type: self.model.encode(text)
            for doc_type, text in self.reference_texts.items()
        }
        logging.info("Reference embeddings created")

    def compute_similarity(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:
        #Calculating cosine similarity between two embeddings
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        logging.debug(f"Computed similarity: {similarity}")
        return similarity

    def classify_document(self, file: ExtractedDoc) -> Tuple[str, float]:
        logging.info(f"Classifying document: {file.file_path}")
        doc_embedding = self.model.encode(file.extracted_text)

        classification_results = {
            doc_type: self.compute_similarity(doc_embedding, ref_embedding)
            for doc_type, ref_embedding in self.reference_embeddings.items()
        }

        logging.debug(f"Classification results: {classification_results}")

        # choose highest similarity of all doc types
        best_match = max(classification_results.items(), key=lambda x: x[1])
        doc_type, confidence = best_match

        # if condidence is too low set type to unknown
        if confidence < config.CONFIDENCE_THRESHOLD:
            doc_type = "unknown"

        logging.info(f"Document classified as {doc_type} with confidence {confidence}")

        return ClassifiedDoc(
            file_name=file.file_path,
            file_type=doc_type,
            confidence=float(confidence),
            processed_at=file.processed_at,
            text_content=file.extracted_text,
            classified_at=datetime.now(),
        )
