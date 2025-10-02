import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# تحميل المتغيرات من .env
load_dotenv()

# تعريف الراوتر
router = APIRouter(prefix="/vlm", tags=["VLM"])

HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# نموذج البيانات
class VLMRequest(BaseModel):
    image_url: str
    prompt: str

@router.post("/analyze")
async def analyze_vlm(request: VLMRequest):
    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": request.prompt},
                        {"type": "image_url", "image_url": {"url": request.image_url}}
                    ]
                }
            ],
        )
        raw_output = completion.choices[0].message.content.strip()

        # 🔹 Remove markdown fences if present
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").replace("json", "", 1).strip()

        # 🔹 Parse JSON safely
        parsed = json.loads(raw_output)

        return {"output": parsed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
