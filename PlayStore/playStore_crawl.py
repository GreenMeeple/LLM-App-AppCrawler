import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Load the CSV file
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv', 'google_playStore.csv')
data = pd.read_csv(src_path)

# Function to scrape the details from a Google Play Store page
def scrape_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the description
        description_tag = soup.find('div', {'class': 'bARER'})
        description = description_tag.text if description_tag else 'N/A'

        # Extract the number of downloads
        downloads_tag = soup.find('div', {'class': 'ClM7O'})
        download = downloads_tag.text if downloads_tag else 'N/A'

        return description, download
    except Exception as e:
        return 'N/A', 'N/A'

# Define the lists to store the crawled data
descriptions = []
downloads = []

# Iterate over each link in the dataframe and scrape details
for link in data['Link']:
    description, download = scrape_details(link)
    descriptions.append(description)
    downloads.append(download)

# Add the scraped data to the dataframe
data['Description'] = descriptions
data['Downloads'] = downloads

# Save the updated dataframe to a new CSV file
dest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv', 'google_playStore_updated.csv')

data.to_csv(dest_path, index=False)

# Output the path to the updated file
print(f"The updated CSV file has been saved to {dest_path}")
