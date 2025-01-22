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

    # Document types and their reference texts
    REFERENCE_TEXTS: Dict[str, str] = field(
        default_factory=lambda: {
            "invoice": """
            Invoice Number Date Amount Total Subtotal Tax Item Quantity Price Terms 
            Due Date Bill Ship Vendor Customer Purchase Order Description 
            Payment Method Reference Number Address Net Currency symbols Discounts Promotions
        """,
            "bank_statement": """
            Account Number Statement Date Beginning Balance Ending Balance Transaction 
            Deposit Withdrawal Interest Fee ACH Check Balance Available Funds Overdraft 
            Bank Name Account Holder Debit Credit Transfer Description Direct Deposit 
            ATM Withdrawal Online Banking Dates
        """,
            "drivers_license": """
            Driver License Number Name Address Date Birth Issue Date Expiration Date 
            State Class Endorsements Restrictions Signature Organ Donor Barcode Photo 
            Gender Height Weight Eye Color Hair Color State Seal License Type Unique identifiers
        """,
        }
    )
    
config = Config()