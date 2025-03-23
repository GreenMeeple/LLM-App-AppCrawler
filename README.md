# AppCrawler

> This Repository is a seperately version of the project [LLM-Powered-App-Challenges](https://github.com/GreenMeeple/LLM-Powered-Apps-Challenges)

## Overview

**AppCrawler** is a Python-based tool designed to collect app data from both the **Apple App Store** and **Google Play Store**. It focuses specifically on applications related to **AI** and **LLMs (Large Language Models)** using curated search keywords and supported country codes.

Collected data is automatically stored in a [MongoDB database](https://www.mongodb.com/products/tools/compass), making it easy to manage, query, and use for downstream tasks.

This crawler is built for further **data analysis**, **market research**, and potential **automation workflows**.

## 🔍 Features

- Crawls apps from **App Store** and **Play Store**
- Uses AI/LLM-related search terms from `search_input.py`
- Filters by countries available on both stores
- Stores the collected data in a MongoDB database
- Gathers data for downstream analysis or automation

### Use Cases

- Track AI/LLM product trends
- Competitor research
- App metadata analysis
- Feed downstream ML or automation pipelines

## 🚀 Getting Started

### Prerequisites

- Python 3.7+ , `pip` for installing packages

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/LLM-App-AppCrawler.git
    cd LLM-App-Automation
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## 🧭 Usage

From the project root, run:

- Apple App Store: `python main.py --store appstore`

- Google Play Store: `python main.py --store playstore`

## 🗃️ Project Details

### Keywords & Country Codes

We have generated the keyword list based on [Google Keyword Planner](https://ads.google.com/intl/en_en/home/tools/keyword-planner/), all keywords and country codes are stored in `util/search_input.py`.

You may modify the list to target different product categories or regions.

### Output & Storage

Collected app data is automatically saved into a MongoDB database. Make sure your MongoDB instance is running and properly configured before running the crawlers.

## 📦 Project Structure

```bash
AppCrawler/
├── main.py                 # Entry point to run the crawlers
├── util/
│   ├── appStore_crawl.py   # iOS App Store crawler
│   ├── playStore_crawl.py  # Google Play Store crawler
│   └── search_input.py     # Contains search keywords and country codes
└── README.md
```
