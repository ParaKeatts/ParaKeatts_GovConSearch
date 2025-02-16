import requests

def main():
    # SAM.gov API endpoint for opportunities search
    url = "https://api.sam.gov/prod/opportunities/v2/search"
    
    # API request parameters
    params = {
        "api_key": "d8VyrOXXzdKKL1deR7vKiQmGhGODsovO7KOsVLJX",
        "q": "small business",
        "postedFrom": "02/16/2024",
        "postedTo": "02/15/2025",
        "limit": 3
    }
    
    # Perform GET request to the API
    response = requests.get(url, params=params)

    # Print the full URL for debugging
    print(f"📡 Request URL: {response.url}")
    print(f"📊 Status Code: {response.status_code}")

    # Handle and print the JSON response or error
    try:
        data = response.json()
        print("\n📂 Response JSON:")
        print(data)

        # Show a quick summary if opportunities exist
        if 'opportunitiesData' in data and len(data['opportunitiesData']) > 0:
            print("\n🔍 Top Opportunities:")
            for i, opp in enumerate(data['opportunitiesData'], 1):
                title = opp.get('title', 'No Title')
                sol_num = opp.get('solicitationNumber', 'No Solicitation Number')
                posted = opp.get('postedDate', 'No Date')
                print(f"{i}. 📝 {title} | Solicitation: {sol_num} | Posted: {posted}")
        else:
            print("\n🚫 No opportunities data found.")
    except Exception as e:
        print(f"❌ Error parsing JSON: {e}")

# Entry point for script execution
if __name__ == "__main__":
    print("🚀 Running SAM.gov Opportunity Search...")
    main()
    print("\n✅ Script Completed.")
