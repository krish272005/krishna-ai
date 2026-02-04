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
