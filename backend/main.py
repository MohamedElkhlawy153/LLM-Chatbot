from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from dotenv import load_dotenv
import os
import requests
import logging

# app
app = FastAPI()

# pydantic
class ChatRequest(BaseModel):
    message: str

# logging
logging.basicConfig(
    filename="../api.log",  
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# load api key from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")
    
#endpoint
@app.post("/chat")
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
            "max_tokens": 500
        }

        
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        # log query and response
        logger.info(f"Query: {query.message}, Response: {result['choices'][0]['message']['content']}")
        
        # response and token count
        return {
            "response": result["choices"][0]["message"]["content"],
            "tokens_used": result.get("usage", {}).get("total_tokens", 0)
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))