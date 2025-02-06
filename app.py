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
        "postedFrom": posted_from,   # e.g., "03/01/2025"
        "postedTo": posted_to,       # e.g., "12/31/2025" (must be in the same year)
        "q": keywords,
        "limit": limit
    }
    if setaside.strip():
        params["setAsideType"] = setaside.strip()
    
    response = requests.get(SAM_API_URL, headers=headers, params=params)
    response.raise_for_status()  # Raise error if something is wrong
    return response.json()

@app.route('/search', methods=['GET'])
def search():
    # Get parameters from the URL query string.
    posted_from = request.args.get('posted_from', '03/01/2025')
    posted_to = request.args.get('posted_to', '12/31/2025')
    keywords = request.args.get('keywords', 'construction OR porta potty')
    setaside = request.args.get('setaside', '')
    try:
        limit = int(request.args.get('limit', 5))
    except ValueError:
        limit = 5

    try:
        data = fetch_opportunities(posted_from, posted_to, keywords, setaside, limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
