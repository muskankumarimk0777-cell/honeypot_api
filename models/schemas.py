"""from pydantic import BaseModel
from typing import Optional

class ScamRequest(BaseModel):
    conversation_id: Optional[str] = "default"
    message: str"""

from pydantic import BaseModel
from typing import Dict, List, Optional


from pydantic import BaseModel
from typing import Dict, List, Optional


class ScamRequest(BaseModel):
    message: Optional[str] = None
    text: Optional[str] = None
    msg: Optional[str] = None
    conversation_id: Optional[str] = None


class ScamResponse(BaseModel):
    scam_detected: bool
    engagement: Dict
    extracted_intelligence: Dict[str, List[str]]
    agent_reply: str
