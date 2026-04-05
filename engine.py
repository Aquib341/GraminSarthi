import os
import easyocr
import numpy as np
import whisper
from PIL import Image
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Ollama
from gtts import gTTS
import base64
from dotenv import load_dotenv

load_dotenv()

class AgriEngine:
    def __init__(self, data_path="data/schemes_db.txt"):
        self.data_path = data_path
        self.vector_db = None
        self.ocr_reader = None
        self.whisper_model = None
        self.llm = None
        
        self._initialize_models()

    def _initialize_models(self):
        print("Engine initialized (Models will lazy-load on first use).")
        # Variables initialized to None in __init__
        pass


    def get_rag_response(self, query, chat_history=None):
        if not self.vector_db:
            print("Loading RAG Database...")
            if os.path.exists(self.data_path):
                loader = TextLoader(self.data_path)
                docs = loader.load()
                text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
                split_docs = text_splitter.split_documents(docs)
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
                self.vector_db = FAISS.from_documents(split_docs, embeddings)
            else:
                return "Knowledge base not initialized."
                
        if not self.llm:
            print("Loading LLM model...")
            self.llm = Ollama(model="llama3")
            
        if chat_history is None:
            chat_history = []
            
        search_query = query
        # If query is short (like 'continue'), append the last meaningful user question for DB logic
        if len(query.strip()) < 15 and len(chat_history) > 0:
            for msg in reversed(chat_history):
                if msg["role"] == "user":
                    search_query = f"{msg['content']} {query}"
                    break
                    
        results = self.vector_db.similarity_search(search_query, k=3) # Increased to fetch more scheme context
        context = "\n".join([res.page_content for res in results]) if results else "No specific context available."
        
        history_str = ""
        for msg in chat_history[-4:]: # Limit the memory to last 4 interactions for speed
            role = "User" if msg["role"] == "user" else "Assistant"
            history_str += f"{role}: {msg['content']}\n"
        
        prompt = f"""System: You are an expert Indian Government Agriculture AI Assistant speaking to farmers.
You MUST follow these strict rules:
1. Answer EXCLUSIVELY in pure Devanagari Hindi script (हिंदी - e.g. किसान बीमा योजना) or standard English-script Hindi (Hinglish). NEVER use Urdu or Arabic script.
2. Provide a HIGHLY detailed, comprehensive explanation. Expand on the information from the context as much as possible.
3. If you are discussing a scheme or agricultural program, you MUST structure your response EXACTLY with these bulleted headings (if the info is available in context, expand on it):
   * **Overview**
   * **Objectives (Uddheshya)**
   * **Benefits (Fayde)**
   * **Eligibility (Patrata)**
   * **Application Process (Avedan Prakriya)**
   * **Documents Required (Zaroori Dastavez)**

Ensure responses are deeply informative, highly detailed, and easy for farmers to understand.

Prior Conversation History:
{history_str}

Context: {context}
User: {query}
Helper:"""
        ans = self.llm.invoke(prompt)
        return ans

    def process_audio_query(self, audio_file_path):
        if not self.whisper_model:
            print("Loading Whisper model...")
            self.whisper_model = whisper.load_model("base")
            
        result = self.whisper_model.transcribe(audio_file_path, language="hi")
        # Removing the LLM 'linguist' interceptor because it was hallucinating input intent.
        # RAG vectorization handles fuzzy Whisper text much more accurately natively.
        return result["text"]

    def process_ocr(self, image_input):
        if not self.ocr_reader:
            print("Loading EasyOCR...")
            self.ocr_reader = easyocr.Reader(['hi', 'en'])
        
        # image_input can be a file path or PIL Image
        if isinstance(image_input, str):
            img = Image.open(image_input)
        else:
            img = image_input
            
        txt_list = self.ocr_reader.readtext(np.array(img), detail=0)
        full_txt = " ".join(txt_list)
        return full_txt

    def analyze_document(self, ocr_text):
        if not self.llm:
            print("Loading LLM model for Doc Analysis...")
            from langchain_community.llms import Ollama
            self.llm = Ollama(model="llama3")

        if len(ocr_text.strip()) < 5:
            return "❌ Nahi, is photo mein koi clear text nahi dikh raha hai. Yeh shayad ek galat document ya dhundhla (blurry) photo hai. Kripya saaf photo khinchein."

        prompt = f"""System: You are an expert Indian Government Document Analyzer. 
Analyze the following text extracted from an OCR scan of a user's uploaded photo. 
1. Identify the likely document type (e.g., Aadhaar card, PAN card, Khasra/Khatauni Land Record, Bank Passbook, Voter ID, etc.). If it looks like garbage or a random unreadable photo, strictly state that it is an invalid document.
2. State clearly if this document is USEFUL for applying to agricultural schemes (like PM-Kisan, KCC).
You MUST answer exclusively in pure Devanagari Hindi or standard English-script Hindi (Hinglish). Do NOT use Urdu script. 

Extracted Text: {ocr_text}
Analysis:"""
        ans = self.llm.invoke(prompt)
        return ans

    def check_eligibility(self, state, land, caste, crop):
        eligible = []
        
        # Universal Farmer Schemes
        eligible.append("💳 Kisan Credit Card (KCC) - Up to ₹3 Lakh loan at subsidized interest")
        eligible.append("🚜 PM-Kisan Samman Nidhi - ₹6000 annual income support")

        # North-East / Tribal
        if state in ["Assam", "Meghalaya", "Manipur", "Nagaland"] and caste == "ST":
            eligible.append("☕ Coffee Development Programme (North East Tribal)")
            
        # Social Category specific
        if caste in ["SC", "ST"]:
            eligible.append("🏭 Stand-Up India Scheme (For Agri-Entrepreneurship & SC/ST specific grants)")
            
        # Land holding specific
        if land <= 2.0:
            eligible.append("💧 PMKSY: Per Drop More Crop (Sinchai Subsidy - 55% for Small/Marginal)")
            eligible.append("🌾 SMAM (Agri Mechanization) - Higher Subsidy on Tractors/Tools")
        elif land > 2.0 and land <= 5.0:
            eligible.append("💧 PMKSY: Per Drop More Crop (Sinchai Subsidy - 45% for General)")
        else:
            eligible.append("🏗️ Agriculture Infrastructure Fund (Storage & Post-harvest facilities loans)")

        # Crop specific
        if crop in ["Kharif", "Rabi"]:
            eligible.append("🌾 Pradhan Mantri Fasal Bima Yojana (Crop Insurance)")
            eligible.append("💰 PM-AASHA (Price Support Scheme for Pulses/Oilseeds)")
        elif crop == "Other":
            # Assume Horticulture or Animal Husbandry
            eligible.append("🍎 Mission for Integrated Development of Horticulture (MIDH)")
            eligible.append("🐄 Rashtriya Gokul Mission (Dairy/Animal Husbandry Support)")
            eligible.append("🐟 PM Matsya Sampada Yojana (Fisheries Subsidy)")
            
        # State specific
        if state == "UP":
            eligible.append("🛡️ UP Mukhyamantri Krishak Durghatna Kalyan Yojana")
        elif state == "Bihar":
            eligible.append("⚙️ Bihar Krishi Yantra Subsidy Yojana")
        elif state == "Punjab":
            eligible.append("💧 Punjab Paani Bachao Paise Kamao Scheme")
            
        return eligible

    def text_to_speech_base64(self, text, output_filename="response.mp3"):
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(output_filename)
        with open(output_filename, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
        return b64

    def get_mandi_prices(self, state, district, commodity):
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        import os
        import datetime
        
        # Load API key from env, fallback to public demo key for Agmarknet API limits
        api_key = os.getenv("MANDI_API_KEY", "579b464db66ec23bdd000001db83f20366c64a55576340be90bd1ac4")
        
        print(f"Fetching Mandi Prices for {commodity} in {district}, {state}")
        
        try:
            url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            params = {
                "api-key": api_key,
                "format": "json",
                "filters[state]": state.title(),
                "filters[district]": district.title(),
                "filters[commodity]": commodity.title(),
                "limit": 10
            }
            
            # Setup session with retry logic
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            session = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
            session.mount('https://', HTTPAdapter(max_retries=retries))
            
            # Use 30 second timeout instead of 10 and add verify=False for local libressl compatibility
            response = session.get(url, params=params, timeout=30, verify=False)
            
            # If the API key is not authorized, the Data.gov.in API often returns 200 OK with an error payload
            data = response.json()
            if "error" in data:
                return {"error": f"API Error: {data.get('error', 'Unknown Error')}. Please verify the MANDI_API_KEY in your .env file or register at data.gov.in."}
                
            response.raise_for_status()
            
            if "records" in data and len(data["records"]) > 0:
                # Sort by arrival_date to get the latest
                records = data["records"]
                try:
                    records.sort(key=lambda x: datetime.datetime.strptime(x.get("arrival_date", "01/01/1970"), "%d/%m/%Y"), reverse=True)
                except Exception:
                    pass # Keep order if parse fails

                latest = records[0]
                return {
                    "state": latest.get("state", state),
                    "district": latest.get("district", district),
                    "commodity": latest.get("commodity", commodity),
                    "min_price": latest.get("min_price", "N/A"),
                    "max_price": latest.get("max_price", "N/A"),
                    "modal_price": latest.get("modal_price", "N/A"),
                    "arrival_date": latest.get("arrival_date", "Today")
                }
            else:
                raise requests.exceptions.RequestException(f"No recent market data recorded for {commodity} in {district}")
        except requests.exceptions.RequestException as e:
            # Fallback to realistic mock data if API limits are reached or servers are down
            print(f"Mandi API Error: {e}. Falling back to recent estimated data.")
            
            # Generate realistic base prices
            bases = {
                "Wheat": 2300, "Rice": 3200, "Soyabean": 5000, "Tomato": 2000,
                "Onion": 2800, "Paddy(Dhan)": 3200, "Cotton": 7000, "Maize": 2200,
                "Potato": 1800, "Mustard": 5200, "Garlic": 12000, "Gram": 5800, "Bajra": 2500
            }
            base = bases.get(commodity.title(), 2000)
            
            if commodity.title() == "Soyabean":
                min_p = "2100"
                max_p = "5610"
                modal_p = "4999"
            else:
                min_p = str(int(base * 0.85))
                max_p = str(int(base * 1.15))
                modal_p = str(base)
            
            return {
                "state": state,
                "district": district,
                "commodity": commodity,
                "min_price": min_p,
                "max_price": max_p,
                "modal_price": modal_p,
                "arrival_date": "Today (Estimated Offline API Data)"
            }

    def get_fertilizer_shops_map(self, state, district):
        import requests
        import folium
        from folium.plugins import MarkerCluster
        
        # Get coordinates of the district using Nominatim
        headers = {'User-Agent': 'GraminAI/1.0 (Contact: local@example.com)'}
        query = f"{district}, {state}, India"
        nom_url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
        
        try:
            nom_res = requests.get(nom_url, headers=headers, timeout=10).json()
            if not nom_res:
                return None, 0
                
            lat = float(nom_res[0]['lat'])
            lon = float(nom_res[0]['lon'])
            
            # Overpass query to find fertilizer/agrarian shops around 50km
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f'''
            [out:json][timeout:25];
            (
              node["shop"="agrarian"](around:50000,{lat},{lon});
              way["shop"="agrarian"](around:50000,{lat},{lon});
              relation["shop"="agrarian"](around:50000,{lat},{lon});
            );
            out center;
            '''
            op_res = requests.get(overpass_url, params={'data': overpass_query}, timeout=30).json()
            
            m = folium.Map(location=[lat, lon], zoom_start=10, tiles='OpenStreetMap')
            
            # Add a marker for the district center
            folium.Marker([lat, lon], popup=f"{district} Center", icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
            
            marker_cluster = MarkerCluster().add_to(m)
            
            count = 0
            if 'elements' in op_res:
                for element in op_res['elements']:
                    count += 1
                    if element['type'] == 'node':
                        elat = element['lat']
                        elon = element['lon']
                    else:
                        elat = element['center']['lat']
                        elon = element['center']['lon']
                        
                    name = element.get('tags', {}).get('name', 'Govt/Local Fertilizer Shop')
                    folium.Marker(
                        [elat, elon],
                        popup=name,
                        icon=folium.Icon(color='green', icon='leaf')
                    ).add_to(marker_cluster)
                    
            return m, count
        except Exception as e:
            print(f"Error generating map: {e}")
            return None, 0

    def get_weather_forecast(self, state, district):
        import requests
        
        try:
            # Get coordinates using open-meteo geocoding (reliable JSON format)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={district}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url, timeout=10)
            
            try:
                geo_data = geo_res.json()
            except Exception:
                return {"error": "Weather service API is unreachable. Please try again later."}
                
            if "results" not in geo_data or len(geo_data["results"]) == 0:
                return {"error": f"Coordinates not found for {district}, {state}"}
                
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            
            # Fetch Weather from Open-Meteo with current conditions added
            meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
            weather_res = requests.get(meteo_url, timeout=10)
            
            try:
                weather_data = weather_res.json()
            except Exception:
                return {"error": "Failed to parse weather API response."}
            
            if "daily" in weather_data:
                return {
                    "daily": weather_data["daily"],
                    "current": weather_data.get("current", {}),
                    "location": f"{district}, {state}"
                }
            else:
                return {"error": "Weather data not available from API."}
        except Exception as e:
            return {"error": f"Failed to fetch weather: {e}"}

# Singleton instance to be shared across fastapi/streamlit
engine = None

def get_engine():
    global engine
    if engine is None:
        engine = AgriEngine()
    return engine
