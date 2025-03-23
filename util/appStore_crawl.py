import requests
from pymongo import MongoClient
import time
from util.search_input import country_codes, keywords

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
 
# Function to search apps using iTunes Search API for a specific region
def search_itunes_store(keyword, country='us', limit=1000):
    search_url = f"https://itunes.apple.com/search?term={keyword}&entity=software&limit={limit}&country={country}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to prepare the app data for MongoDB insertion
def prepare_app_data(app, keyword):
    return {
        "title": app.get('trackName', ''),
        "developer": app.get('sellerName', ''),
        "score": app.get('averageUserRating', 0),
        "description": app.get('description', ''),
        "developer_url": app.get('sellerUrl', ''),
        "app_url": app.get('trackViewUrl', ''),
        "keyword": keyword,
        "license": app.get('isVppDeviceBasedLicensingEnabled', False),
        "price": app.get('price', 0),
        "language": app.get('languageCodesISO2A', []),
        "age_rating": app.get('trackContentRating', ''),
        "releaseDate": app.get('releaseDate', ''),
        "rating_count": app.get('userRatingCount', 0),
        "bundle_ID": app.get('bundleId', ''),
    }

# MongoDB connection and data processing
def run_as():
    with MongoClient('mongodb://localhost:27017/') as client:
        db = client['Thesis_data']
        collection = db['Apple_AppStore']

        for country, code in country_codes.items():
            for keyword in keywords:
                print(f"Searching for '{keyword}' in '{country}'")
                try:
                    results = search_itunes_store(keyword, country=code, limit=1000)
                    apps = results.get('results', [])
                    
                    if not apps:
                        print(f"No results found for '{keyword}' in the '{country}'.")
                        continue  # Skip to the next keyword

                    for app in apps:
                        app_data = prepare_app_data(app, keyword)
                        collection.update_one(
                            {"appId": app.get('trackId')},
                            {"$set": app_data},
                            upsert=True
                        )
                    
                    time.sleep(1)  # Add delay between requests to avoid rate limiting

                except requests.exceptions.RequestException as req_err:
                    print(f"Request error for '{keyword}' in '{country}': {req_err}")
                except Exception as e:
                    print(f"Error processing '{keyword}' in '{country}': {e}")

                time.sleep(2)

    print("Data has been successfully imported into MongoDB.")