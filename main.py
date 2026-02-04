from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI(title="Krishna AI", version="2.0")

with open("principles.json", "r", encoding="utf-8") as f:
    PRINCIPLES = json.load(f)

class Question(BaseModel):
    message: str

# AI internal state
ai_state = {
    "stage": "listening",  # listening → analyzing → guiding
    "context": ""
}

@app.get("/")
def home():
    return {"status": "Krishna AI is awake 🦚"}

@app.post("/chat")
def chat(q: Question):
    user_input = q.message.lower()

    # 1️⃣ ANALYSIS PHASE
    if ai_state["stage"] == "listening":
        ai_state["context"] = user_input
        ai_state["stage"] = "analyzing"

        return {
            "reply": (
                "Arjuna, main tumhari baat sun raha hoon.\n"
                "Par pehle yeh batao:\n\n"
                "Tumhara man bhay se bhara hai,\n"
                "ya kartavya ko lekar duvidha mein ho?"
            )
        }

    # 2️⃣ DECISION PHASE
    if ai_state["stage"] == "analyzing":
        if "bhay" in user_input or "dar" in user_input:
            ai_state["stage"] = "guiding"
            decision = "fear"
        else:
            ai_state["stage"] = "guiding"
            decision = "duty"

        return {
            "reply": (
                "Tumhari baaton se mujhe spasht ho raha hai.\n\n"
                "Yeh samasya **{}** se judi hai.\n\n"
                "Ab dhyan se suno, main tumhe marg dikhaunga."
            ).format(decision)
        }

    # 3️⃣ GUIDANCE PHASE
    if ai_state["stage"] == "guiding":
        ai_state["stage"] = "listening"

        return {
            "reply": (
                "Karm tumhara adhikar hai,\n"
                "phal tumhara bandhan nahi.\n\n"
                "Jo sahi hai use karo,\n"
                "par parinam ka bojh chhod do.\n\n"
                "Ab jao, aur apne kartavya par dridh raho."
            )
        }
from fastapi import FastAPI
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load principles
with open("principles.json", "r", encoding="utf-8") as f:
    PRINCIPLES = json.load(f)

class UserMessage(BaseModel):
    message: str

def detect_state(text: str):
    text = text.lower()
    if any(word in text for word in ["scared", "afraid", "fear"]):
        return "dar"
    if any(word in text for word in ["confused", "lost", "confusion"]):
        return "bhram"
    if any(word in text for word in ["fail", "failure"]):
        return "asafalta"
    if any(word in text for word in ["anxious", "anxiety", "worried"]):
        return "chinta"
    return "general"

def select_principle(state: str):
    for p in PRINCIPLES:
        if state in p["use_when"]:
            return p["principle"]
    return "Man ko shaant karna hi pehla karm hai"

def krishna_response(user_text: str):
    state = detect_state(user_text)
    principle = select_principle(state)

    response = f"""
Tum apne vicharon se vyakul ho,
kyunki tumhara man bhay aur aasakti se bandha hai.

Yahi bandhan tumhari drishti ko dhundhla kar raha hai.

Is satya ko samjho:
{principle}

Isliye karm se peeche mat hato.
Jo tumhara kartavya hai, use shaant aur sthir man se karo.
Phal ko apne man ka bojh mat banao.
""".strip()

    return response

@app.post("/chat")
def chat(data: UserMessage):
    reply = krishna_response(data.message)
    return {"reply": reply}
