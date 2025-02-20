from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta

def scrape_newtimes(query, max_pages=5):
    search_url = f'https://www.newtimes.co.rw/search?query={query}'
    print(f"Search URL: {search_url}")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--headless')  # Run in background
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--incognito")
    options.add_argument('--disable-gpu')  # Disable GPU usage
    options.binary_location = "/usr/bin/google-chrome"  # Path to Chrome binary

    driver = None
    results = []
    try:
        print("Setting up ChromeDriver service...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("ChromeDriver service started.")
        
        for page in range(1, max_pages + 1):
            print(f"Navigating to {search_url} (page {page})...")
            driver.get(f"{search_url}&pgno={page}")
            print("Page loaded.")

            print("Waiting for search results to load...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'nt-search-widget'))
            )
            print("Search results loaded.")

            articles = driver.find_elements(By.CLASS_NAME, 'article')
            print(f"Found {len(articles)} articles on page {page}")

            if not articles:
                print("No articles found. Printing page source for debugging:")
                print(driver.page_source)

            for article in articles:
                try:
                    title = article.find_element(By.CLASS_NAME, 'article-title').text
                    link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    snippet = article.find_element(By.CLASS_NAME, 'article-section').text
                    date_text = article.find_element(By.CLASS_NAME, 'article-date').text
                    article_date = datetime.strptime(date_text, '%A, %B %d, %Y')

                    # Check if the article is within the past 3 months
                    if article_date >= datetime.now() - timedelta(days=90):
                        results.append({'title': title, 'link': link, 'snippet': snippet, 'date': article_date})
                        print(f"Extracted article: Title: {title}, Link: {link}, Snippet: {snippet}, Date: {article_date}")
                except Exception as e:
                    print(f"Error extracting article: {e}")

            # Wait a bit before loading the next page to avoid being blocked
            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
        if driver:
            print(driver.page_source)  # Print the page source for debugging

    finally:
        if driver:
            driver.quit()
    
    return results