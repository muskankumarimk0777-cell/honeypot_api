SCAM_KEYWORDS = [
    "otp", "upi", "bank", "blocked",
    "verify", "urgent", "refund", "link",
    "kyc pending",
    "account blocked",
    "verify now",
    "urgent",
    "click immediately"
]

def detect_scam(text: str) -> bool:
    text = text.lower()
    score = sum(1 for k in SCAM_KEYWORDS if k in text)
    return score >= 2
