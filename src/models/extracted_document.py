from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class ExtractedDoc:
    """Document model - after extraction"""

    file_path: str
    extracted_text: str
    processed_at: datetime

    def to_dict(self) -> Dict:
        return {
            "file_path": self.file_path,
            "extracted_text": self.extracted_text,
            "processed_at": self.processed_at.isoformat(),
        }
