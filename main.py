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
