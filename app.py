from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
print("Flask App Created")

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["github_webhooks"]
events_collection = db["events"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    try:
        if event_type == "push":
            author = data.get("pusher", {}).get("name")
            to_branch = data.get("ref", "").split("/")[-1]
            timestamp = datetime.utcnow().isoformat()

            events_collection.insert_one({
                "author": author,
                "action": "PUSH",
                "to_branch": to_branch,
                "timestamp": timestamp
            })

        elif event_type == "pull_request":
            action = data.get("action")
            pr_data = data.get("pull_request", {})

            if action == "opened":
                author = pr_data.get("user", {}).get("login")
                from_branch = pr_data.get("head", {}).get("ref")
                to_branch = pr_data.get("base", {}).get("ref")
                timestamp = pr_data.get("created_at")

                events_collection.insert_one({
                    "author": author,
                    "action": "PULL_REQUEST",
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": timestamp
                })

            elif action == "closed" and pr_data.get("merged"):
                author = pr_data.get("user", {}).get("login")
                from_branch = pr_data.get("head", {}).get("ref")
                to_branch = pr_data.get("base", {}).get("ref")
                timestamp = pr_data.get("merged_at")

                events_collection.insert_one({
                    "author": author,
                    "action": "MERGE",
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": timestamp
                })

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 400

@app.route("/events", methods=["GET"])
def get_events():
    latest = list(events_collection.find().sort("timestamp", -1).limit(10))
    for e in latest:
        e["_id"] = str(e["_id"])  # Convert ObjectId to string
    return jsonify(latest)

if __name__ == "__main__":
    print("Starting the flask server..")
    app.run(debug=True)
