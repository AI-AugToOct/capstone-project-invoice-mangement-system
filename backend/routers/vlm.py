import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("❌ HF_TOKEN not found in .env")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

router = APIRouter(prefix="/vlm", tags=["VLM"])

class AnalyzeRequest(BaseModel):
    image_url: str
    prompt: str

class AnalyzeResponse(BaseModel):
    output: str

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": req.prompt},
                        {"type": "image_url", "image_url": {"url": req.image_url}}
                    ]
                }
            ]
        )

        message = completion.choices[0].message
        result = message.get("content") if isinstance(message, dict) else message.content
        return {"output": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling HuggingFace VLM: {str(e)}")
