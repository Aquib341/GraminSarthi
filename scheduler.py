import schedule
import time
import datetime
from database import get_all_users
from engine import get_engine

# Initialize the engine to use its functions
agri_engine = get_engine()

# Mock Scheme Deadlines Database for the demo
SCHEME_DEADLINES = {
    "PMKSY": {"name": "PMKSY (Sinchai Subsidy)", "deadline": datetime.date.today() + datetime.timedelta(days=2)},
    "FASAL_BIMA": {"name": "Pradhan Mantri Fasal Bima Yojana", "deadline": datetime.date.today() + datetime.timedelta(days=5)},
}

def send_whatsapp_alert(phone_number, message):
    """
    Mock function to simulate sending a WhatsApp message via Twilio.
    """
    print(f"\n[TWILIO MOCK] Sending WhatsApp to {phone_number}:")
    print(f"Message: {message}\n")

def check_and_send_alerts():
    print(f"\n[{datetime.datetime.now()}] Running Daily Smart Alerts Check...")
    users = get_all_users()
    
    if not users:
        print("No users found in database.")
        return

    today = datetime.date.today()

    for user in users:
        alerts = []
        
        # 1. Scheme Deadline Alerts (The "Nudge" Engine)
        for scheme_id, scheme_data in SCHEME_DEADLINES.items():
            days_left = (scheme_data["deadline"] - today).days
            if days_left == 2:
                alerts.append(f"⚠️ Nudge: Only {days_left} days left to apply for {scheme_data['name']}! Deadline is {scheme_data['deadline'].strftime('%d %B')}.")
        
        # 2. Daily Mandi Price Alert
        if user["primary_crop"] and user["district"]:
            # Fetch prices using the core engine
            price_data = agri_engine.get_mandi_prices(user["state"], user["district"], user["primary_crop"])
            alerts.append(f"📈 Today's Mandi Price for {user['primary_crop']} in {user['district']}:\nModal Price: ₹{price_data['modal_price']}/Quintal\nMin-Max: ₹{price_data['min_price']} - ₹{price_data['max_price']}")

        # Send aggregated alerts to the user
        if alerts:
            message = f"Namaste {user['name']},\n\nHere are your Jan-Swayam AI updates for today:\n\n" + "\n\n".join(alerts)
            send_whatsapp_alert(user["phone_number"], message)


def start_scheduler():
    # Schedule to run every day at 08:00 AM
    schedule.every().day.at("08:00").do(check_and_send_alerts)
    
    # Also for demonstration, schedule to run every minute
    schedule.every(1).minutes.do(check_and_send_alerts)
    
    print("Scheduler started. Waiting for scheduled jobs...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
