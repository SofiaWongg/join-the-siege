from dataclasses import dataclass
from datetime import datetime

@dataclass
class ClassifiedDoc:
    """Document after classification"""
    file_name: str
    file_type: str
    confidence: float
    processed_at: datetime
    text_content: str
    classified_at: datetime


    def to_dict(self) -> dict:
        return {
            "file_name": self.file_name,
            "file_type": self.file_type,
            "confidence": float(self.confidence),
            "processed_at": self.processed_at.isoformat(),
            "text_content": self.text_content,
            "classified_at": self.classified_at.isoformat()
        }