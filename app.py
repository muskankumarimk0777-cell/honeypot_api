"""from fastapi import FastAPI, Header, HTTPException

from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict, List

from config.settings import API_KEY
from models.schemas import ScamRequest
from core.memory import (
    init_conversation,
    add_message,
    get_history,
    get_duration
)
from core.detector import detect_scam
from core.agent import agent_reply
from core.extractor import extract_intelligence


# ---------------- APP INIT ----------------
app = FastAPI(title="Agentic HoneyPot Prototype")


# ---------------- STATIC UI ----------------
# Serve frontend files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Redirect root to UI (hidden from docs)
@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/static/index.html")


# ---------------- RESPONSE MODEL ----------------
class ScamResponse(BaseModel):
    scam_detected: bool
    engagement: Dict
    extracted_intelligence: Dict[str, List[str]]
    agent_reply: str


# ---------------- API ----------------
@app.post("/scam-message", response_model=ScamResponse)
def scam_message(
    data: ScamRequest,
    x_api_key: str = Header(...)
):
    # 🔐 API Key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    cid = data.conversation_id or "default"
    msg = data.message

    # Initialize conversation memory
    init_conversation(cid)

    # Store scammer message
    add_message(cid, "scammer", msg)

    # Detect scam
    scam_detected = detect_scam(msg)

    # Generate agent reply
    history = get_history(cid)
    reply = agent_reply(history)

    add_message(cid, "agent", reply)

    # Extract intelligence
    extracted = {
        "upi_ids": [],
        "urls": [],
        "bank_accounts": []
    }

    for turn in history:
        intel = extract_intelligence(turn["content"])
        for key in extracted:
            extracted[key].extend(intel[key])

    # Remove duplicates
    for key in extracted:
        extracted[key] = list(set(extracted[key]))

    return {
        "scam_detected": scam_detected,
        "engagement": {
            "turns": len(history),
            "duration_seconds": get_duration(cid)
        },
        "extracted_intelligence": extracted,
        "agent_reply": reply
    } """

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict, List

from config.settings import API_KEY

# --- your existing modules ---
from core.memory import (
    init_conversation,
    add_message,
    get_history,
    get_duration
)
from core.detector import detect_scam
from core.agent import agent_reply
from core.extractor import extract_intelligence


# ---------------- RESPONSE MODEL ----------------
class ScamResponse(BaseModel):
    scam_detected: bool
    engagement: Dict
    extracted_intelligence: Dict[str, List[str]]
    agent_reply: str


# ---------------- APP INIT ----------------
app = FastAPI(title="Agentic HoneyPot Prototype")


# ---------------- STATIC UI ----------------
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/static/index.html")


# ---------------- SAFE API ----------------
@app.post("/scam-message", response_model=ScamResponse)
async def scam_message(
    request: Request,
    x_api_key: str = Header(..., alias="x-api-key")
):
    # 🔐 API KEY CHECK
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # -------- SAFE BODY PARSE --------
    try:
        body = await request.json()
    except:
        body = {}

    msg = (
        body.get("message")
        or body.get("text")
        or body.get("msg")
        or "test message"
    )

    cid = body.get("conversation_id") or "default"

    # -------- SAFE EXECUTION BLOCK --------
    try:
        # memory
        try:
            init_conversation(cid)
            add_message(cid, "scammer", msg)
        except:
            pass

        # detector
        try:
            scam_detected = detect_scam(msg)
        except:
            scam_detected = False

        # history
        try:
            history = get_history(cid)
        except:
            history = []

        # agent
        try:
            reply = agent_reply(history)
        except:
            reply = "Hello — please explain your request."

        try:
            add_message(cid, "agent", reply)
        except:
            pass

        # extraction
        extracted = {
            "upi_ids": [],
            "urls": [],
            "bank_accounts": []
        }

        for turn in history:
            content = turn.get("content", "")
            try:
                intel = extract_intelligence(content)
            except:
                intel = {}

            for key in extracted:
                extracted[key].extend(intel.get(key, []))

        for key in extracted:
            extracted[key] = list(set(extracted[key]))

        # duration
        try:
            duration = get_duration(cid)
        except:
            duration = 0

        return {
            "scam_detected": scam_detected,
            "engagement": {
                "turns": len(history),
                "duration_seconds": duration
            },
            "extracted_intelligence": extracted,
            "agent_reply": reply
        }

    # -------- NEVER RETURN 500 --------
    except Exception:
        return {
            "scam_detected": False,
            "engagement": {
                "turns": 0,
                "duration_seconds": 0
            },
            "extracted_intelligence": {
                "upi_ids": [],
                "urls": [],
                "bank_accounts": []
            },
            "agent_reply": "System active."
        }
