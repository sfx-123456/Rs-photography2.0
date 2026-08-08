from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pathlib import Path
import csv

app = Flask(__name__, template_folder=".", static_folder=".")
BOOKINGS = Path("bookings.csv")

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/book")
def book():
    data = request.get_json(silent=True) or {}
    required = ["name", "email", "phone", "shoot_type"]
    if any(not str(data.get(k, "")).strip() for k in required):
        return jsonify(message="Please complete all required fields."), 400

    exists = BOOKINGS.exists()
    with BOOKINGS.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "date", "name", "email", "phone", "shoot_type", "message"
        ])
        if not exists:
            writer.writeheader()
        writer.writerow({
            "date": datetime.now().isoformat(timespec="seconds"),
            "name": data["name"].strip(),
            "email": data["email"].strip(),
            "phone": data["phone"].strip(),
            "shoot_type": data["shoot_type"].strip(),
            "message": str(data.get("message", "")).strip()
        })

    return jsonify(message="Booking request received. We'll contact you soon!")

if __name__ == "__main__":
    app.run(debug=True)
