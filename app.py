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
        "postedFrom": posted_from,    # e.g., "2024-01-01"
        "postedTo": posted_to,      # e.g., "2025-12-31"
        "q": urllib.parse.quote(keywords),  # FIX: Properly encode keywords
        "limit": limit
    }
    if setaside.strip():
        params["setAsideType"] = setaside.strip()

    print(f"DEBUG: Sending request to SAM.gov API with params: {params}") # DEBUGGING: Log parameters

    try:
        response = requests.get(SAM_API_URL, headers=headers, params=params)
        response.raise_for_status()    # Raise HTTPError for bad responses (4xx or 5xx)

        try: # TRY TO PARSE JSON, CATCH JSONDecodeError SPECIFICALLY
            data = response.json()
            print("DEBUG: SAM.gov API response (JSON):") # DEBUGGING: Indicate JSON response
            # We will NOT print the entire JSON here to keep the output clean, but we know it's JSON now
            return data
        except json.JSONDecodeError as json_err: # Catch JSON parsing errors
            print("DEBUG: JSONDecodeError from SAM.gov API response!") # DEBUGGING: Indicate JSON decode error
            print("DEBUG: Raw Response Text from SAM.gov API:") # DEBUGGING: Print raw response text
            print(response.text) # DEBUGGING: Print raw response text
            return {"error": f"Error decoding JSON response from SAM.gov API: {str(json_err)}", "raw_response_text": response.text}, 500 # Return 500 and raw text

    except requests.exceptions.RequestException as req_err: # Catch request exceptions (network issues, timeouts, etc.)
        print(f"DEBUG: RequestException to SAM.gov API: {str(req_err)}") # DEBUGGING: Log request exception
        return {"error": f"API request failed: {str(req_err)}"}, 500 # Return 500 for request errors

@app.route('/search', methods=['GET'])
def search():
    # Get parameters from the URL query string.
    posted_from = request.args.get('posted_from', '2024-01-01')
    # FIX: Ensure posted_to is in YYYY-MM-DD format - default to today + 1 year for example
    posted_to = request.args.get('posted_to', '2025-02-08') # Changed default to YYYY-MM-DD format
    keywords = request.args.get('keywords', 'construction OR porta potty')
    setaside = request.args.get('setaside', '')

    try:
        limit = int(request.args.get('limit', 5))
    except ValueError:
        limit = 5

    # Debugging: Print the exact request before sending it
    print(f"DEBUG: Sending request to SAM.gov -> {SAM_API_URL}")
    print(f"Params: {json.dumps({'postedFrom': posted_from, 'postedTo': posted_to, 'q': keywords, 'limit': limit}, indent=2)}")

    try:
        data = fetch_opportunities(posted_from, posted_to, keywords, setaside, limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Debugging: Print the exact request before sending it
    print(f"DEBUG: Sending request to SAM.gov -> {SAM_API_URL}")
    print(f"Params: {json.dumps({'postedFrom': posted_from, 'postedTo': posted_to, 'q': keywords, 'limit': limit}, indent=2)}")

    try:
        data = fetch_opportunities(posted_from, posted_to, keywords, setaside, limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
