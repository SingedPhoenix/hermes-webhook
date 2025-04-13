
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Hermes Webhook is Live"

@app.route("/webhook", methods=["POST"])
def receive_webhook():
    try:
        data = request.json
        print("📩 Webhook Received from Notion")

        # Log basic metadata (customize later)
        notion_event = data.get("event", {})
        event_type = notion_event.get("type", "unknown")
        page_id = notion_event.get("data", {}).get("id", "N/A")
        timestamp = notion_event.get("data", {}).get("last_edited_time", "N/A")

        print(f"Event Type: {event_type}")
        print(f"Page ID: {page_id}")
        print(f"Last Edited: {timestamp}")

        return jsonify({"status": "Hermes received"}), 200

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
