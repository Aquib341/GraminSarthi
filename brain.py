from fastapi import FastAPI, UploadFile, File, Form, Request, Response
from pydantic import BaseModel
from engine import get_engine
import io
import os
import requests
from PIL import Image
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI(title="Jan-Swayam AI Backend")
agri_engine = get_engine()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_jan_swayam(request: QueryRequest):
    """
    Takes a text query and returns a RAG-based answer in Hinglish.
    """
    response = agri_engine.get_rag_response(request.query)
    return {"answer": response}

@app.post("/scan")
async def scan_document(file: UploadFile = File(...)):
    """
    Takes an image upload (Aadhaar, Land Records, etc.) and extracts text using EasyOCR.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    extracted_data = agri_engine.process_ocr(image)
    return {"extracted_data": extracted_data}

@app.post("/eligibility")
async def check_eligibility(state: str = Form(...), land: float = Form(...), caste: str = Form(...), crop: str = Form(...)):
    """
    Checks scheme eligibility based on user profile data.
    """
    eligible_schemes = agri_engine.check_eligibility(state, land, caste, crop)
    return {"eligible_schemes": eligible_schemes}

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Twilio Webhook for incoming WhatsApp messages.
    Handles Text AND Voice Notes.
    """
    form_data = await request.form()
    body = form_data.get("Body", "").strip()
    media_url = form_data.get("MediaUrl0", "")
    media_content_type = form_data.get("MediaContentType0", "")

    response = MessagingResponse()
    msg = response.message()

    try:
        if media_url and "audio" in media_content_type:
            # Handle Voice Note
            audio_response = requests.get(media_url)
            temp_audio_path = "temp_whatsapp_audio.ogg"
            with open(temp_audio_path, "wb") as f:
                f.write(audio_response.content)
            
            # Process with Whisper
            user_query = agri_engine.process_audio_query(temp_audio_path)
            
            # Get RAG Answer
            bot_reply = agri_engine.get_rag_response(user_query)
            
            # Cleanup
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                
            msg.body(f"🗣️ You asked: {user_query}\n\n🤖 Answer: {bot_reply}")
            
        elif body:
            # Handle Text Query
            bot_reply = agri_engine.get_rag_response(body)
            msg.body(bot_reply)
        else:
            msg.body("Please send a text message or a voice note.")
            
    except Exception as e:
        print(f"Error processing WhatsApp message: {e}")
        msg.body("Kshama karein, ek takneeki samasya aayi hai. Kripya thodi der baad prayas karein.")

    return Response(content=str(response), media_type="application/xml")

# Route placeholder for Mandi Prices
@app.get("/prices")
async def get_mandi_prices(state: str, district: str, commodity: str):
    """
    Fetches real-time Mandi prices using the Govt API.
    """
    prices = agri_engine.get_mandi_prices(state, district, commodity)
    return {"status": "success", "data": prices}
