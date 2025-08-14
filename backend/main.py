from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
import os
import requests
import logging
from typing import Optional
from datetime import datetime

# تحميل المتغيرات البيئية قبل كل شيء
load_dotenv()

# التحقق من المتغيرات البيئية المطلوبة
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")

if not GROQ_API_KEY or not GROQ_API_URL:
    raise ValueError("GROQ_API_KEY and GROQ_API_URL must be set in .env file")

# إعداد التطبيق
app = FastAPI(
    title="Chatbot API",
    description="AI Chatbot API with GROQ integration",
    version="1.0.0"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# نماذج البيانات
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace")
        return v.strip()

class ChatResponse(BaseModel):
    response: str
    tokens_used: int
    timestamp: str

# إعداد السجلات
logging.basicConfig(
    filename="/app/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# التحقق من صحة الاتصال بـ GROQ
def verify_groq_connection():
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        response = requests.get(f"{GROQ_API_URL}/models", headers=headers)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"GROQ API connection error: {str(e)}")
        return False

@app.on_event("startup")
async def startup_event():
    if not verify_groq_connection():
        logger.error("Failed to connect to GROQ API")
        # التطبيق سيستمر في العمل ولكن مع تسجيل الخطأ

@app.post("/chat", response_model=ChatResponse)
async def chat(query: ChatRequest):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "يرجى دائمًا الرد بنفس لغة السؤال سواء كانت بالعربية أو الإنجليزية."
                },
                {
                    "role": "user",
                    "content": query.message
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7,  # إضافة درجة الحرارة للتحكم في الإبداعية
            "top_p": 0.9       # إضافة top_p للتحكم في التنوع
        }

        response = requests.post(
            GROQ_API_URL,
            json=payload,
            headers=headers,
            timeout=30  # إضافة timeout
        )
        response.raise_for_status()
        result = response.json()

        # تسجيل الطلب والاستجابة
        logger.info(
            f"Query: {query.message}, "
            f"Response: {result['choices'][0]['message']['content']}, "
            f"Tokens: {result.get('usage', {}).get('total_tokens', 0)}"
        )

        return ChatResponse(
            response=result["choices"][0]["message"]["content"],
            tokens_used=result.get("usage", {}).get("total_tokens", 0),
            timestamp=datetime.now().isoformat()
        )

    except requests.exceptions.Timeout:
        logger.error("Request to GROQ API timed out")
        raise HTTPException(status_code=504, detail="Request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"GROQ API request error: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")