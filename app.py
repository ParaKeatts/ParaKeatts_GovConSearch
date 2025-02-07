from flask import Flask, request, jsonify
import json
import requests
import urllib.parse

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
        "q": urllib.parse.quote(keywords),
        "limit": limit
    }
    if setaside.strip():
        params["setAsideType"] = setaside.strip()

    print(f"DEBUG: Sending request to SAM.gov API with params: {params}")

    try:
        response = requests.get(SAM_API_URL, headers=headers, params=params)
        response.raise_for_status()

        try:
            data = response.json()
            print("DEBUG: SAM.gov API response (JSON):")
            return data
        except json.JSONDecodeError as json_err:
            print("DEBUG: JSONDecodeError from SAM.gov API response!")
            print("DEBUG: Raw Response Text from SAM.gov API:")
            print(response.text)
            return {"error": f"Error decoding JSON: {str(json_err)}", "raw_response": response.text}, 500

    except requests.exceptions.RequestException as req_err:
        print(f"DEBUG: RequestException to SAM.gov API: {str(req_err)}")
        return {"error": f"API Request Failed: {str(req_err)}"}, 500

@app.route('/search', methods=['GET'])
def search():
    # Get parameters from the URL query string, ensuring correct date format (YYYY-MM-DD).
    posted_from = request.args.get('posted_from', '2024-01-01') # Default is already YYYY-MM-DD
    posted_to = request.args.get('posted_to', '2025-02-08')   # Default is now YYYY-MM-DD

    keywords = request.args.get('query', 'construction OR porta potty') # Corrected parameter name to 'query' to match OpenAPI spec
    setaside = request.args.get('setaside', '')

    try:
        limit = int(request.args.get('limit', 5))
    except ValueError:
        limit = 5

    print(f"DEBUG: Request to /search endpoint received.") # Debugging log
    print(f"DEBUG: Parameters received: query='{keywords}', posted_from='{posted_from}', posted_to='{posted_to}', limit={limit}, setaside='{setaside}'") # Debugging log

    try:
        data = fetch_opportunities(posted_from, posted_to, keywords, setaside, limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
