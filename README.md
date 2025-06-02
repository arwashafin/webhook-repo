# Webhook Receiver for GitHub Events 

This Flask application receives GitHub webhook events (Push, Pull Request, Merge), stores them in MongoDB and displays the most recent events in a clean, minimal web interface.

## Key Features

- Receives GitHub webhook events via `/webhook` endpoint
- Supports:
  -  Push events
  -  Pull Requests (opened)
  -  Merge detection via closed PRs with `"merged": true`
- Stores events in MongoDB
- Displays recent events in human-readable format on UI
- Frontend polls every 15 seconds for updates
- Built with Flask, MongoDB, HTML/JS

## 💡 LLM Smart Prompting Highlights

As per the assessment instructions, the following parts were efficiently implemented using LLM prompting:
- Simplifying GitHub webhook JSON - Prompted for extracting only essential fields like author, branch, timestamp
- Detecting PR merge vs open
- Timestamp formatting - Asked LLM to convert ISO to readable UTC string in JavaScript
- Minimal UI - Prompted LLM for polling HTML layout with clean design 
- MongoDB schema - Generated a compact event schema: type, author, from_branch, to_branch, timestamp

---

##  Tech Stack

- Python Flask
- MongoDB
- JavaScript + HTML (no frontend framework)
- Flask-CORS for API access

