from pymongo import MongoClient
from google_play_scraper import app, search
import time
from util.search_input import country_codes, keywords

# MongoDB connection setup
def run_ps():
    with MongoClient('mongodb://localhost:27017/') as client:
        db = client['Thesis_data']
        collection = db['google_playStore']  # Single collection for all apps

        for country, code in country_codes.items():
            for keyword in keywords:
                try:
                    print(f"Searching for '{keyword}' in '{country}'")
                    results = search(keyword, country=code)

                    if results is None:
                        print(f"No results found for '{keyword}' in {country}.")
                        continue
                    limited_results = results[:1000]

                    for search_result in limited_results:
                        full_result = app(
                            search_result['appId'],
                            lang='en', # defaults to 'en'
                            country='us' # defaults to 'us'
                        )
                        
                        # Upsert (update if exists, otherwise insert)
                        collection.update_one(
                            {"appId": full_result['appId']},
                            {
                                "$set": {
                                    "title": full_result['title'],
                                    "released": full_result.get('released', ''),
                                    "installs": full_result.get('realInstalls', ''),
                                    "score": full_result.get('score', ''),
                                    "results of": keyword     ,                           
                                    "originalPrice": full_result.get('originalPrice', '') ,
                                    "inAppProductPrice": full_result.get('inAppProductPrice', '') ,
                                    "currency": full_result.get('currency', '') ,
                                    "contentRating": full_result.get('contentRating', '') ,
                                    "contentRatingDescription": full_result.get('contentRatingDescription', '') ,
                                    "adSupported": full_result.get('adSupported', '') ,
                                    "genreId": full_result.get('genreId', '') ,
                                    "developer": full_result['developer'],
                                    "url": full_result.get('url', ''),
                                    "developerWebsite": full_result.get('developerWebsite', '') ,
                                    "categories": full_result.get('categories', '') ,
                                    "description": full_result.get('description', ''),
                                },
                                "$addToSet": {"countries": country}  # Ensure no duplicate countries
                            },
                            upsert=True
                        )
                except Exception as e:
                    print(f"Error searching for '{keyword}' in {country}: {e}")
                time.sleep(1)

        print("Data has been successfully imported into MongoDB.")