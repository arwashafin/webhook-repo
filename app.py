from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.github_events
events = db.events

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook received!")
    print("Headers:", request.headers)
    print("Payload:", request.json)
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json
    print("Recieved:", payload)

    try:
        if event_type == "push":
            author = payload["pusher"]["name"]
            to_branch = payload["ref"].split("/")[-1]
            timestamp = datetime.utcnow().isoformat()
            events.insert_one({
                "type": "PUSH",
                "author": author,
                "to_branch": to_branch,
                "timestamp": timestamp
            })

        elif event_type == "pull_request":
            action = payload["action"]
            pr = payload["pull_request"]
            author = pr["user"]["login"]
            from_branch = pr["head"]["ref"]
            to_branch = pr["base"]["ref"]
            if action == "opened":
                events.insert_one({
                    "type": "PULL_REQUEST",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": pr["created_at"]
                })
            elif action == "closed" and pr["merged"]:
                events.insert_one({
                    "type": "MERGE",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": pr["merged_at"]
                })

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/events', methods=['GET'])
def get_events():
    docs = events.find().sort("timestamp", -1).limit(10)
    result = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        result.append(doc)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)


    
