import os
import requests
import pandas as pd

# Function to search apps using iTunes Search API for a specific region
def search_itunes_store(keyword, country='us', limit=10):
    # Construct the search URL with the country parameter
    search_url = f"https://itunes.apple.com/search?term={keyword}&entity=software&limit={limit}&country={country}"
    
    # Send a request to get the search results
    response = requests.get(search_url)
    response.raise_for_status()  # Check if the request was successful
    search_results = response.json()
    
    # Extract app details
    app_names = []
    app_developers = []
    app_descriptions = []
    app_ratings = []
    app_links = []

    for result in search_results.get('results', []):
        app_names.append(result.get('trackName', 'N/A'))
        app_developers.append(result.get('artistName', 'N/A'))
        app_descriptions.append(result.get('description', 'N/A'))
        app_ratings.append(result.get('averageUserRating', 'N/A'))
        app_links.append(result.get('trackViewUrl', 'N/A'))

    # Create a DataFrame
    data = pd.DataFrame({
        'App Name': app_names,
        'Developer': app_developers,
        'Ratings': app_ratings,
        'Description': app_descriptions,
        'Link': app_links,
    })
    
    return data

# Get keyword and country input from the user
keyword = input("Enter the keyword to search for: ")
country = input("Enter the country code (e.g., 'us' for United States, 'gb' for United Kingdom): ")

# Search the iTunes Store
app_data = search_itunes_store(keyword, country=country, limit=1000)


# Save the data to a CSV file
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv', 'appStore.csv')
app_data.to_csv(output_path, index=False)

# Output the path to the saved file
print(f"The search results have been saved to {output_path}")
