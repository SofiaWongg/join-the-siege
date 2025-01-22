from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Config:
    """Application configuration"""
    # API settings
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max-size

    # Model settings
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    CONFIDENCE_THRESHOLD: float = 0.3

    # File settings - dataclasses are immutable so we need field
    ALLOWED_EXTENSIONS: List[str] = field(default_factory=lambda: ["pdf", "png", "jpg"])


config = Config()