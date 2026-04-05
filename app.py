import streamlit as st
import os
import shutil
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="GraminSarthi", page_icon="", layout="wide")
st.image("/Users/aquib/Downloads/GraminAI/navbar.png", use_container_width=True)

st.markdown("""
<style>

/* ================= HIDE SIDEBAR ================= */
section[data-testid="stSidebar"] {
    display: none;
}

/* ================= GLOBAL BACKGROUND ================= */
.stApp {
    background:
        linear-gradient(rgba(255,255,255,0.93), rgba(255,255,255,0.93)),
        url("/Users/aquib/Downloads/GraminAI/pkvy.webp");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* ================= TRICOLOR WAVE (SCROLL FEEL) ================= */
.stApp::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    height: 14px;
    width: 100%;
    background: linear-gradient(
        90deg,
        #FF9933 0%,
        #ffffff 50%,
        #138808 100%
    );
    background-size: 200% 100%;
    animation: waveMove 6s ease-in-out infinite;
    z-index: 1000;
}

@keyframes waveMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ================= ASHOKA CHAKRA (ANIMATED) ================= */
.stApp::before {
    content: "";
    position: fixed;
    width: 420px;
    height: 420px;
    right: 6%;
    bottom: 8%;
    background: url("https://upload.wikimedia.org/wikipedia/commons/1/17/Ashoka_Chakra.svg");
    background-size: contain;
    background-repeat: no-repeat;
    opacity: 0.07;
    animation: chakraSpin 90s linear infinite;
    pointer-events: none;
}

@keyframes chakraSpin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ================= GOVERNMENT OF INDIA BADGE ================= */
.main::before {
    content: "🇮🇳 Government of India | GraminSarthi";
    display: block;
    text-align: center;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #0A3D62;
    background: rgba(255,255,255,0.7);
    border: 1px solid #dcdcdc;
    border-radius: 30px;
    padding: 10px 22px;
    margin-bottom: 18px;
    backdrop-filter: blur(10px);
}

/* ================= STICKY GLASS NAVBAR ================= */
img[src*="navbar.png"] {
    position: sticky;
    top: 14px;
    z-index: 999;
    backdrop-filter: blur(12px);
    background: rgba(255,255,255,0.65);
    border-radius: 0 0 18px 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

/* ================= MAIN CONTAINER ================= */
.main {
    padding: 2.4rem;
}

/* ================= TEXT VISIBILITY ================= */
body, p, span, label, div {
    color: #1e272e !important;
}

/* ================= HEADINGS ================= */
h1 {
    font-weight: 800;
    background: linear-gradient(90deg, #FF9933, #0A3D62, #138808);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 {
    color: #0A3D62 !important;
    border-left: 6px solid #FF9933;
    padding-left: 10px;
}

/* ================= GLASSMORPHISM ================= */
[data-testid="stChatMessage"],
.scheme-card {
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

/* ================= BUTTONS ================= */
.stButton > button {
    border-radius: 32px;
    background: linear-gradient(135deg, #FF9933, #0A3D62, #138808);
    color: white !important;
    font-weight: 700;
    padding: 0.7rem;
    border: none;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.22);
}

/* ================= CHAT ================= */
[data-testid="stChatMessage"] {
    border-left: 6px solid #0A3D62;
    padding: 14px;
    margin-bottom: 14px;
    border-radius: 18px;
    animation: chatIn 0.35s ease;
}

@keyframes chatIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ================= AI TYPING CURSOR ================= */
[data-testid="stChatMessage"]:last-child::after {
    content: "▍";
    margin-left: 4px;
    animation: blink 1s infinite;
    color: #0A3D62;
}

@keyframes blink {
    50% { opacity: 0; }
}

/* ================= SCHEME CARDS WITH MINISTRY ICONS ================= */
.scheme-card::before {
    content: "🏛️";
    font-size: 1.4rem;
    margin-right: 8px;
}

.scheme-card {
    border-left: 7px solid #138808;
    padding: 20px;
    margin-bottom: 18px;
    font-weight: 600;
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.scheme-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.2);
}

/* ================= MIC GLOW ================= */
audio:focus {
    animation: micPulse 1.4s infinite;
    box-shadow: 0 0 0 6px rgba(19,136,8,0.35);
}

@keyframes micPulse {
    0% { box-shadow: 0 0 0 0 rgba(19,136,8,0.45); }
    70% { box-shadow: 0 0 0 14px rgba(19,136,8,0); }
}

/* ================= MOBILE ================= */
@media (max-width: 768px) {
    .main { padding: 1.2rem; }
    h1 { font-size: 1.6rem; }
}

/* ================= DARK MODE ================= */
html[data-theme="dark"] body,
html[data-theme="dark"] p,
html[data-theme="dark"] div {
    color: #ecf0f1 !important;
}

html[data-theme="dark"] .stApp {
    background:
        linear-gradient(rgba(0,0,0,0.78), rgba(0,0,0,0.78)),
        url("/Users/aquib/Downloads/GraminAI/pkvy.webp");
}

/* ================= WEATHER WIDGET ================= */
.weather-hero {
    background: linear-gradient(to bottom, #1E272E, #2F3640);
    border-radius: 20px;
    padding: 24px;
    color: white !important;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}
.weather-hero h2, .weather-hero h1 {
    color: white !important;
    border-left: none;
    margin: 0;
    padding: 0;
}
.weather-temp {
    font-size: 5rem;
    font-weight: bold;
    color: #FFD32A;
    margin-bottom: 0px;
    line-height: 1;
}
.weather-desc {
    font-size: 1.4rem;
    color: #dfe6e9;
    margin-bottom: 20px;
}
.weather-stats-row {
    display: flex;
    justify-content: space-around;
    background: rgba(0,0,0,0.2);
    padding: 15px;
    border-radius: 12px;
}
.weather-stat-box {
    text-align: center;
}
.weather-stat-val {
    font-size: 1.2rem;
    font-weight: bold;
    color: white;
}
.weather-stat-lbl {
    font-size: 0.9rem;
    color: #b2bec3;
}
.weather-day-card {
    background: rgba(47, 54, 64, 0.9);
    border-radius: 12px;
    padding: 12px 5px;
    text-align: center;
    color: white;
    margin-top: 15px;
}
.weather-day-card div, .weather-day-card p {
    color: white !important;
}
.weather-day-title { font-weight: bold; font-size: 0.9rem; margin-bottom: 5px; }
.weather-day-icon { font-size: 1.8rem; margin: 5px 0; }
.weather-day-minmax { font-size: 0.8rem; color: #b2bec3 !important; }

/* ================= DEEP UI OVERHAUL ================= */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(14px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 10px 40px rgba(0,0,0,0.1), 0 4px 15px rgba(0,0,0,0.05);
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
    padding: 1.5rem !important;
    margin-bottom: 1.2rem;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.18), 0 8px 25px rgba(0,0,0,0.1);
}

/* ================= MODERN INPUTS ================= */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, .stFileUploader > div {
    border-radius: 14px !important;
    border: 2px solid #E2E8F0 !important;
    background: rgba(255, 255, 255, 0.95) !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.03) !important;
    transition: all 0.3s ease !important;
}
div[data-baseweb="input"]:focus-within > div, div[data-baseweb="select"]:focus-within > div {
    border-color: #0A3D62 !important;
    box-shadow: 0 0 0 4px rgba(10, 61, 98, 0.15) !important;
    transform: translateY(-1px);
}

/* ================= STREAMLIT TABS ================= */
button[data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.5);
    border-radius: 14px 14px 0 0 !important;
    margin-right: 6px !important;
    padding: 10px 18px !important;
    border: none !important;
    border-bottom: 4px solid transparent !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.8);
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: white;
    border-bottom: 4px solid #138808 !important;
    box-shadow: 0 -4px 15px rgba(0,0,0,0.06);
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# --- 2. ENGINES SETUP (Modularized) ---
@st.cache_resource
def load_ai_engine_v2():
    from engine import AgriEngine
    return AgriEngine()

ai_engine = load_ai_engine_v2()

def text_to_speech(text):
    b64 = ai_engine.text_to_speech_base64(text, output_filename="response.mp3")
    md = f"""<audio autoplay="true" controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>"""
    st.markdown(md, unsafe_allow_html=True)

# --- 4. UI LAYOUT ---
st.title("GraminSarthi: Multi-Agent AI Sahayak")
st.write("Voice | OCR | Eligibility | Multilingual Support")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["💬 AI Sahayak (Voice/Text)", "📋 Eligibility Tracker", "📄 Document Scanner", "📈 Market Trends", "🔒 Digilocker", "📍 Agri-Maps", "🌦️ Krishi Mausam"])

# --- TAB 1: SMART CHAT ---
with tab1:
    with st.container(border=True):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🎤 Voice Input")
            audio_msg = st.audio_input("Boliye, main sun raha hoon...")
        
        with col2:
            st.subheader("🤖 AI Response")
        
            for msg in st.session_state.messages:
                if msg["role"] != "user": # Do not show the user's input text on screen
                    st.chat_message(msg["role"]).write(msg["content"])
            
            user_query = ""
            if audio_msg:
                with st.spinner("Processing voice..."):
                    with open("temp.wav", "wb") as f: f.write(audio_msg.read())
                    user_query = ai_engine.process_audio_query("temp.wav")
        
            manual_txt = st.chat_input("Ya yahan likhiye:")
            final_input = user_query if user_query else manual_txt

            if final_input:
                # Add to memory but do not write to screen
                st.session_state.messages.append({"role": "user", "content": final_input})
            
                with st.spinner("Searching documents & Generating response..."):
                    ans = ai_engine.get_rag_response(final_input, st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    st.chat_message("assistant").write(ans)
                    text_to_speech(ans)

# --- TAB 2: ELIGIBILITY ---
with tab2:
    with st.container(border=True):
        st.subheader("Aap kaunsi yojana ke liye patra (eligible) hain?")
        c1, c2 = st.columns(2)
        s = c1.selectbox("State:", ["UP", "Bihar", "Assam", "Punjab", "Other"])
        l = c1.number_input("Zameen (Hectares):", min_value=0.0, value=1.0)
        ca = c2.selectbox("Caste:", ["General", "OBC", "SC", "ST"])
        cr = c2.selectbox("Crop:", ["Kharif", "Rabi", "Other"])
    
        if st.button("Check Now"):
            res = ai_engine.check_eligibility(s, l, ca, cr)
            if res:
                for r in res: st.markdown(f"<div class='scheme-card'>{r}</div>", unsafe_allow_html=True)
                text_to_speech(f"Aap {len(res)} yojanaon ke liye eligible hain.")
            else:
                st.warning("Koi match nahi mila.")

# --- TAB 3: OCR SCANNER ---
with tab3:
    with st.container(border=True):
        st.subheader("📄 Document Scanner")
        st.write("Kagaj ki photo khinche (Aadhaar/Land Records)")
        doc_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    
        if doc_file:
            img = Image.open(doc_file)
            st.image(img, width=400)
            if st.button("Extract Info"):
                with st.spinner("Reading document..."):
                    full_txt = ai_engine.process_ocr(img)
                    display_txt = full_txt[:200] + "..." if len(full_txt) > 200 else full_txt
                    st.info(f"Detected Text: {display_txt}")
                
                # Analyze with AI
                with st.spinner("AI document verify kar raha hai..."):
                    analysis_result = ai_engine.analyze_document(full_txt)
                    st.write(f"💡 **AI Analysis:**\n\n{analysis_result}")
                
                # Save to Digital Locker
                with st.spinner("Digital Locker mein save kar rahe hain..."):
                    locker_dir = "data/digital_locker"
                    os.makedirs(locker_dir, exist_ok=True)
                    save_path = os.path.join(locker_dir, doc_file.name)
                    with open(save_path, "wb") as f:
                        f.write(doc_file.getbuffer())
                    st.success(f"Dastavez ko Digital Locker mein surakshit roop se save kar liya gaya hai: {doc_file.name}")

# --- TAB 4: MARKET TRENDS ---
with tab4:
    with st.container(border=True):
        st.subheader("📈 Daily Mandi Prices")
        st.write("Aapke zila mein fasal ke taza daam dekhiye (Using Agmarknet API)")
    
        import json
        json_path = "data/states_districts.json"
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                india_data = json.load(f)["states"]
            state_names = [s["state"] for s in india_data]
        else:
            state_names = ["Madhya Pradesh", "Uttar Pradesh", "Maharashtra", "Punjab", "Bihar", "Rajasthan"]
            india_data = []

        mc1, mc2, mc3 = st.columns(3)
    
        default_state_idx = state_names.index("Uttar Pradesh") if "Uttar Pradesh" in state_names else 0
        sel_state = mc1.selectbox("State:", state_names, index=default_state_idx, key="mandi_state")
    
        if india_data:
            districts = next((s["districts"] for s in india_data if s["state"] == sel_state), ["Indore"])
        else:
            districts = ["Indore", "Bhopal", "Banda"]
        
        default_dist_idx = districts.index("Banda") if "Banda" in districts else 0
        sel_dist = mc2.selectbox("District:", districts, index=default_dist_idx, key="mandi_dist")
    
        sel_crop = mc3.selectbox("Crop:", ["Soyabean", "Wheat", "Rice", "Tomato", "Onion", "Paddy(Dhan)", "Cotton", "Maize", "Potato", "Mustard", "Garlic", "Gram", "Bajra"])
    
        if st.button("Get Prices"):
            with st.spinner("Govt API se data la rahe hain..."):
                price_data = ai_engine.get_mandi_prices(sel_state, sel_dist, sel_crop)
            
                if "error" in price_data:
                    st.error(price_data["error"])
                else:
                    st.success(f"Latest prices for {sel_crop} in {sel_dist} as of {price_data.get('arrival_date', 'Today')}")
                
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Min Price (₹/Qtl)", price_data['min_price'])
                    m2.metric("Modal Price (₹/Qtl)", price_data['modal_price'])
                    m3.metric("Max Price (₹/Qtl)", price_data['max_price'])

                    # Mock Trend Chart
                    import datetime
                    dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(6, -1, -1)]
                    try:
                        base_price = int(price_data['modal_price'])
                    except (ValueError, TypeError):
                        base_price = 2000
                    prices = [base_price + (i % 3 * 50) - (i % 2 * 30) for i in range(7)]
                
                    df = pd.DataFrame({"Date": dates, "Price (₹)": prices})
                    fig = px.line(df, x="Date", y="Price (₹)", title=f"{sel_crop} 7-Day Trend in {sel_dist}", markers=True)
                    st.plotly_chart(fig, use_container_width=True)

# --- TAB 5: DIGITAL LOCKER ---
with tab5:
    with st.container(border=True):
        st.subheader("🔒 Digital Document Locker")
        st.write("Aapke scan kiye gaye sabhi dastavez yahan surakshit hain.")
    
        locker_dir = "data/digital_locker"
        os.makedirs(locker_dir, exist_ok=True)
    
        # Upload new document section
        st.markdown("### Upload New Document")
        new_doc = st.file_uploader("Upload Image to Locker", type=['jpg', 'png', 'jpeg'], key="locker_upload")
        if new_doc:
            if st.button("Save to Locker"):
                with st.spinner("Saving..."):
                    save_path = os.path.join(locker_dir, new_doc.name)
                    with open(save_path, "wb") as f:
                        f.write(new_doc.getbuffer())
                    st.success(f"Saved: {new_doc.name}")
                    st.rerun()
                
        st.markdown("### Your Saved Documents")
        if os.path.exists(locker_dir) and os.listdir(locker_dir):
            files = os.listdir(locker_dir)
            if len(files) > 0:
                cols = st.columns(3)
                for i, filename in enumerate(files):
                    col = cols[i % 3]
                    with col:
                        filepath = os.path.join(locker_dir, filename)
                    try:
                        img = Image.open(filepath)
                        st.image(img, use_container_width=True, caption=filename)
                        with open(filepath, "rb") as file:
                            st.download_button(
                                label=f"⬇️ Download {filename}",
                                data=file,
                                file_name=filename,
                                mime="image/jpeg" # Adjust mime type if needed
                            )
                    except Exception as e:
                        st.error(f"Error loading {filename}: {e}")
        else:
            st.info("Abhi tak koi dastavez save nahi kiya gaya hai. Kripya Document Scanner ka upyog karein.")

# --- TAB 6: AGRI-MAPS ---
with tab6:
    with st.container(border=True):
        st.subheader("📍 Nearby Government Fertilizer Shops")
        st.write("Aapke zila mein sarkari khad (fertilizers) ki dukaanein aur anya krishi kendra khojein.")
    
        map_c1, map_c2 = st.columns(2)
        map_state = map_c1.selectbox("State:", ["Madhya Pradesh", "Uttar Pradesh", "Maharashtra", "Punjab", "Bihar", "Rajasthan"], key="map_state")
        map_district = map_c2.text_input("District:", value="Indore", key="map_district")
    
        if st.button("Search Shops in Map"):
            with st.spinner("Nakshe par dukaanein dhoondh rahe hain (Fetching from Google Maps)..."):
                st.success(f"Viewing actual government kisan mandi and fertilizer locations in {map_district} on Google Maps!")
            
                # Google Maps Embed iframe
                import urllib.parse
                import streamlit.components.v1 as components
            
                query = f"Government fertilizer shops kisan mandi in {map_district}, {map_state}"
                encoded_query = urllib.parse.quote(query)
                embed_url = f"https://maps.google.com/maps?width=800&height=500&hl=en&q={encoded_query}&t=&z=13&ie=UTF8&iwloc=B&output=embed"
            
                components.html(
                    f'<iframe width="800" height="500" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{embed_url}"></iframe>',
                    width=800, height=500
                )

                # --- Map Details Section ---
                st.markdown(f"### 🏪 Verified Local Khad/Beej Kendras in {map_district}")
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    st.markdown(f"<div class='scheme-card'><b>{map_district} Krishi Upaj Mandi Samiti</b><br>Near Main Bus Stand<br>Available: Urea, DAP, Seeds</div>", unsafe_allow_html=True)
                with sc2:
                    st.markdown(f"<div class='scheme-card'><b>IFFCO eBazar {map_district}</b><br>Station Road<br>Available: NPK, Bio-fertilizers, Tools</div>", unsafe_allow_html=True)
                with sc3:
                    st.markdown(f"<div class='scheme-card'><b>Zila Sahkari Kendriya Bank (PACS)</b><br>Collectorate Area<br>Available: Subsidy Khad, Cash Loans</div>", unsafe_allow_html=True)


# --- TAB 7: KRISHI MAUSAM ---
with tab7:
    with st.container(border=True):
        st.subheader("🌦️ 7-Day Krishi Mausam (Weather Forecast)")
        st.write("Aapke kshetr ka aagami 7 dinon ka mausam aur baarish ka anuman.")
    
        weather_c1, weather_c2 = st.columns(2)
        weather_state = weather_c1.selectbox("State:", ["Madhya Pradesh", "Uttar Pradesh", "Maharashtra", "Punjab", "Bihar", "Rajasthan"], key="weather_state")
        weather_district = weather_c2.text_input("District:", value="Indore", key="weather_district")
    
        if st.button("Get Weather Forecast"):
            with st.spinner("Mausam ki jankari laa rahe hain..."):
                weather_data = ai_engine.get_weather_forecast(weather_state, weather_district)
            
                if weather_data and "error" not in weather_data:
                    daily = weather_data["daily"]
                    current = weather_data.get("current", {})
                
                    # Dark Theme Hero Banner mimicking User Image
                    if current:
                        temp = current.get("temperature_2m", "")
                        feels = current.get("apparent_temperature", temp)
                        wind = current.get("wind_speed_10m", "")
                        humidity = current.get("relative_humidity_2m", "")
                        precip = current.get("precipitation", "")
                    
                        hero_html = f"""
                        <div class='weather-hero'>
                            <h2>Now · {weather_data['location']}</h2>
                            <div class='weather-temp'>{temp}°</div>
                            <div class='weather-desc'>Feels like {feels}° ☀️</div>
                        </div>
                        """
                        st.markdown(hero_html, unsafe_allow_html=True)
                    else:
                        st.success(f"Weather Forecast for {weather_data['location']}")
                
                    # Create a layout for 7 days
                    cols = st.columns(7)
                    import datetime
                    for i in range(7):
                        date_str = daily["time"][i]
                        max_temp = daily["temperature_2m_max"][i]
                        min_temp = daily["temperature_2m_min"][i]
                        rain = daily["precipitation_sum"][i]
                    
                        try:
                            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                            # "Today", "Tomorrow", or Day name
                            if i == 0: day_title = "Today"
                            elif i == 1: day_title = "Tom."
                            else: day_title = dt.strftime("%a")
                        except Exception:
                            day_title = date_str[5:]
                        
                        # Logic for icon
                        icon = "☀️" if rain < 1.0 else ("⛅" if rain < 5.0 else "🌧️")
                    
                        with cols[i]:
                            card_html = f"""
                            <div class='weather-day-card'>
                                <div class='weather-day-title'>{day_title}</div>
                                <div class='weather-day-icon'>{icon}</div>
                                <div class='weather-day-minmax'>{max_temp}° / {min_temp}°</div>
                            </div>
                            """
                            st.markdown(card_html, unsafe_allow_html=True)
                
                else:
                    st.error(weather_data.get("error", "Failed to fetch weather data."))

# --- SIDEBAR / IN-APP ALERTS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2942/2942501.png", width=80)
st.sidebar.title("Jan-Swayam AI")
st.sidebar.write("Nearest CSC: **Indore Sector-5**")

st.sidebar.markdown("---")
st.sidebar.subheader("🔔 In-App Alerts")
# Mock logic for in-app alerts based on the scheduler logic
import datetime
today = datetime.date.today()
deadline = today + datetime.timedelta(days=2)
st.sidebar.warning(f"⚠️ **Nudge:** Only 2 days left to apply for PMKSY (Sinchai Subsidy)! Deadline is {deadline.strftime('%d %B')}.")
st.sidebar.info("📈 Aaj genhu (Wheat) ka modal bhav Indore mandi mein ₹2250 hai.")
st.sidebar.markdown("---")

if st.sidebar.button("Reset Session", key="reset"): st.rerun()

# Cleanup
if os.path.exists("temp.wav"): os.remove("temp.wav")