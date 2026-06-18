from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import requests

app = Flask(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyC7pruXgt3JAfEL79VdWhQn3aSgI5xzYsY")  # Replace with your key or set environment variable
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        language = data.get("language", "English")

        if not user_message:
            return jsonify({"response": "⚠️ Please type a message before sending."}), 400

        prompt = f"""
You are a helpful public health AI assistant.
- Respond in {language}.
- Keep answers short (2–3 sentences).
- Base answers on trusted sources like WHO, MoHFW, CDC.
- If emergency, advise user to consult a doctor immediately.

User: {user_message}
"""
        response = model.generate_content(prompt)
        return jsonify({"response": response.text if response.text else "⚠️ No response from AI."})

    except Exception as e:
        return jsonify({"response": f"⚠️ Server error: {str(e)}"}), 500


@app.route("/updates", methods=["POST"])
def updates():
    """
    Provide dynamic content for sidebar buttons:
    - alerts: latest regional health alerts
    - schemes: government schemes/yojanas
    - faq: common health FAQs
    """
    try:
        data = request.get_json()
        update_type = data.get("type", "")
        region = data.get("region", "India")

        if update_type == "alerts":
            content = fetch_health_alerts(region)
        elif update_type == "schemes":
            content = fetch_health_schemes(region)
        elif update_type == "faq":
            content = fetch_faqs(region)
        else:
            content = "No data available."

        return jsonify({"response": content})

    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})


def fetch_health_alerts(region):
    """
    Simulate fetching health alerts from Telangana or Odisha govt websites.
    In a real implementation, you would scrape their official pages using requests + BeautifulSoup.
    """
    if region.lower() == "telangana":
        # Example: pretend scraping
        alerts = [
            "1. Dengue outbreak alert in Hyderabad districts.",
            "2. COVID-19 vaccination drive continues in Telangana.",
            "3. Seasonal flu awareness campaign ongoing."
        ]
    elif region.lower() == "odisha":
        alerts = [
            "1. Malaria prevention campaign in coastal districts.",
            "2. Health check-up camps organized in rural Odisha.",
            "3. Awareness drive on safe drinking water."
        ]
    else:
        alerts = ["⚠️ No regional alerts found."]
    return "<br>".join(alerts)


def fetch_health_schemes(region):
    """
    Simulate fetching government health schemes.
    """
    if region.lower() == "telangana":
        schemes = [
            "1. Aarogya Sri Health Insurance Scheme.",
            "2. Telangana State Nutrition Mission.",
            "3. Free Health Checkups for senior citizens."
        ]
    elif region.lower() == "odisha":
        schemes = [
            "1. Biju Swasthya Kalyan Yojana.",
            "2. Odisha State Health Insurance for BPL families.",
            "3. Maternal & Child Health programs."
        ]
    else:
        schemes = ["✅ No schemes found."]
    return "<br>".join(schemes)


def fetch_faqs(region):
    """
    Provide some generic health FAQs.
    """
    faqs = [
        "1. What should I do if I have a fever? → Drink fluids and consult a doctor if it persists.",
        "2. How can dengue be prevented? → Avoid mosquito bites, remove stagnant water.",
        "3. Can cold/flu spread person to person? → Yes, through droplets; maintain hygiene."
    ]
    return "<br>".join(faqs)


if __name__ == "__main__":
    app.run(debug=True)
