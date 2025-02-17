from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

# SAM.gov API Endpoint and Key
SAM_API_URL = "https://api.sam.gov/opportunities/v2/search"
SAM_API_KEY = "oKpuXpOIzjJkxNSjhel3G42yJEsmszLLlqJUjhhc"

headers = {
    "Accept": "application/json",
    "x-api-key": SAM_API_KEY
}

def fetch_opportunities(posted_from, posted_to, keywords, setaside, limit=5):
    params = {
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "q": keywords,  # Removed urllib.parse.quote to prevent encoding issues
        "limit": str(limit),  # Ensure limit is a string
        "type": "opp"  # Ensures we only get active opportunities
    }

    if setaside.strip():
        params["setAsideType"] = setaside.strip()

    print(f"DEBUG: Sending request to SAM.gov API with params: {params}")

    try:
        response = requests.get(SAM_API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"DEBUG: HTTP Error from SAM.gov API: {str(http_err)}")
        return {"error": f"HTTP Error: {str(http_err)}"}, response.status_code
    except requests.exceptions.RequestException as req_err:
        print(f"DEBUG: RequestException to SAM.gov API: {str(req_err)}")
        return {"error": f"API Request Failed: {str(req_err)}"}, 500

@app.route('/')
def home():
    return jsonify({"message": "GovCon AI API is running! Use /search to query bids."})

@app.route('/search', methods=['GET'])
def search():
    # Extract query parameters from request
    posted_from = request.args.get('posted_from', '2024-01-01')
    posted_to = request.args.get('posted_to', '2025-02-08')
    keywords = request.args.get('query', 'construction OR porta potty')  # Defaults to broad search
    setaside = request.args.get('setaside', '')

    try:
        limit = int(request.args.get('limit', 5))
    except ValueError:
        limit = 5  # Default limit if user input is invalid

    print(f"DEBUG: Request to /search received: query='{keywords}', posted_from='{posted_from}', posted_to='{posted_to}', limit={limit}, setaside='{setaside}'")

    try:
        data = fetch_opportunities(posted_from, posted_to, keywords, setaside, limit)
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
