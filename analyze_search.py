import pandas as pd
from datetime import datetime
import time
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib.parse
from search_config import SITES

class DocsSearchAnalyzer:
    def __init__(self, site_key):
        if site_key not in SITES:
            raise ValueError(f"Unknown site key: {site_key}. Available sites: {', '.join(SITES.keys())}")
            
        self.config = SITES[site_key]
        self.site_name = self.config["name"]
        print(f"Initializing search analyzer for {self.site_name}...")
        self.results = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Selenium WebDriver with Chrome in headless mode."""
        print("Setting up Chrome driver...")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        print("Initializing Chrome driver...")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        print("Chrome driver setup complete!")
        
    def load_search_phrases(self, filename="search_phrases.txt"):
        """Load search phrases from a file."""
        print(f"Loading search phrases from {filename}...")
        try:
            with open(filename, 'r') as file:
                phrases = [line.strip() for line in file if line.strip()]
                print(f"Loaded {len(phrases)} search phrases")
                return phrases
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            sys.exit(1)

    def analyze_search(self, phrase):
        """Analyze search results for a given phrase."""
        print(f"\nAnalyzing search results for: '{phrase}'")
        try:
            # Construct the search URL with proper encoding
            encoded_phrase = urllib.parse.quote(phrase)
            search_url = f"{self.config['base_url']}{self.config['search_path']}?{self.config['search_query_param']}={encoded_phrase}"
            print(f"Navigating to: {search_url}")
            self.driver.get(search_url)
            
            # Wait for search results to load
            try:
                print("Waiting for search results to load...")
                # Wait for the search results list to load
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.config['selectors']['result_container'])))
                time.sleep(self.config['page_load_delay'])  # Additional delay to ensure all results are loaded
                
                # Get all search result items
                search_results = self.driver.find_elements(By.CSS_SELECTOR, self.config['selectors']['result_container'])
                print(f"Found {len(search_results)} results")
                
                current_date = datetime.now().strftime("%Y-%m-%d")
                
                # Process up to max_results
                for position, result in enumerate(search_results[:self.config['max_results']], 1):
                    try:
                        # Get the title link element
                        title_link = result.find_element(By.CSS_SELECTOR, self.config['selectors']['result_title'])
                        title = title_link.text.strip()
                        url = title_link.get_attribute("href")
                        
                        # Extract section information from the title
                        section_parts = title.split(" | ", 1)
                        section = section_parts[0].strip("b<>")
                        page_title = section_parts[1] if len(section_parts) > 1 else title
                        
                        # Skip empty results
                        if not title or not url:
                            continue
                            
                        print(f"Result {position}: {section} | {page_title}")
                        
                        self.results.append({
                            'date': current_date,
                            'site': self.site_name,
                            'search_phrase': phrase,
                            'result_url': url,
                            'section': section,
                            'page_title': page_title,
                            'position': position
                        })
                    except Exception as e:
                        print(f"Error processing result {position} for '{phrase}': {e}")
                        continue
                        
            except TimeoutException:
                print(f"No results found for '{phrase}' or page took too long to load")
                
        except Exception as e:
            print(f"Error analyzing search for '{phrase}': {e}")
            return None

    def save_analysis(self, filename=None):
        """Save analysis results to a CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            site_key = self.site_name.lower().replace(" ", "_")
            filename = f"search_analysis_{site_key}_{timestamp}.csv"
        
        print(f"\nSaving {len(self.results)} results to {filename}")
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"Analysis results saved successfully to {filename}")
        
    def cleanup(self):
        """Close the browser and clean up resources."""
        print("\nCleaning up resources...")
        if hasattr(self, 'driver'):
            self.driver.quit()
        print("Cleanup complete!")

def main():
    parser = argparse.ArgumentParser(description='Analyze documentation search results.')
    parser.add_argument('--site', default='upsun', choices=SITES.keys(),
                      help='Which documentation site to analyze (default: upsun)')
    parser.add_argument('--phrases', default='search_phrases.txt',
                      help='File containing search phrases (default: search_phrases.txt)')
    args = parser.parse_args()

    print(f"Starting {SITES[args.site]['name']} Search Analyzer...")
    analyzer = DocsSearchAnalyzer(args.site)
    try:
        search_phrases = analyzer.load_search_phrases(args.phrases)
        
        total_phrases = len(search_phrases)
        print(f"\nStarting analysis process for {total_phrases} phrases")
        
        for i, phrase in enumerate(search_phrases, 1):
            print(f"\nProcessing phrase {i}/{total_phrases}")
            analyzer.analyze_search(phrase)
            time.sleep(SITES[args.site]['delay_between_searches'])  # Delay between searches
        
        analyzer.save_analysis()
    finally:
        analyzer.cleanup()
    print("\nSearch analysis process complete!")

if __name__ == "__main__":
    main() 