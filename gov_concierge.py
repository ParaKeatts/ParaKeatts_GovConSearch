from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

SAM_API_URL = "https://api.sam.gov/prod/opportunities/v2/search"
SAM_API_KEY = "YOUR_SAM_API_KEY"  # Replace with your actual API Key

@app.route("/search", methods=["GET"])
def search_contracts():
    posted_from = request.args.get("posted_from")
    posted_to = request.args.get("posted_to")
    keywords = request.args.get("keywords")
    setaside = request.args.get("setaside", "")
    limit = request.args.get("limit", 5)

    headers = {"Accept": "application/json", "api_key": SAM_API_KEY}
    params = {
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "q": keywords,
        "limit": limit
    }
    
    if setaside.strip():
        params["setAsideType"] = setaside.strip()

    response = requests.get(SAM_API_URL, headers=headers, params=params)
    
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text, "status": response.status_code}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
